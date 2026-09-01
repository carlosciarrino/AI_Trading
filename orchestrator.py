import yfinance as yf
import json, time, os, requests
from datetime import datetime, timezone, timedelta

CONFIG_PATH = os.path.expanduser("~/AI_Trading/config.json")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"
MAX_OPEN_ORDERS = 1
MT4_FILES = os.path.expanduser("~/Scrivania/XM MT4/MQL4/Files")
ORDERS_JSON = os.path.expanduser("~/mt4_shared/orders.json")
OPEN_TIME_FILE = os.path.expanduser("~/mt4_shared/open_time.json")

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def is_trading_hours(session):
    now_utc = datetime.now(timezone.utc).hour
    if session == "all":
        return True
    if session == "london":
        return 8 <= now_utc < 17
    if session == "newyork":
        return 13 <= now_utc < 22
    if session == "tokyo":
        return 0 <= now_utc < 9
    if session == "london_newyork":
        return (8 <= now_utc < 17) or (13 <= now_utc < 22)
    return True

def count_open_orders():
    try:
        with open(ORDERS_JSON) as f:
            orders = json.load(f)
        open_orders = [o for o in orders if o.get('status') == 'open']
        print(f"[DEBUG] Ordini aperti nel file: {len(open_orders)}", flush=True)
        return len(open_orders)
    except Exception as e:
        print(f"[DEBUG] Errore lettura orders.json: {e}", flush=True)
        return 0

def get_signal():
    # 1. Leggi i contesti
    scores = {}
    
    # News
    try:
        with open('/home/carlo/AI_Trading/news_context.txt', 'r') as f:
            text = f.read().lower()
            if any(w in text for w in ['guerra', 'crisi', 'inflazione', 'rialzo tassi']):
                scores['news'] = -0.3
            elif any(w in text for w in ['pace', 'accordo', 'taglio tassi', 'stimoli']):
                scores['news'] = 0.3
            else:
                scores['news'] = 0.0
    except:
        scores['news'] = 0.0
    
    # Social sentiment
    try:
        with open('/home/carlo/AI_Trading/social_context.txt', 'r') as f:
            text = f.read().lower()
            if 'positivo' in text:
                scores['social'] = 0.2
            elif 'negativo' in text:
                scores['social'] = -0.2
            else:
                scores['social'] = 0.0
    except:
        scores['social'] = 0.0
    
    # Cicli stagionali
    try:
        with open('/home/carlo/AI_Trading/cycles_context.txt', 'r') as f:
            text = f.read().lower()
            import re
            month = datetime.now().month
            lines = text.split('\n')
            for line in lines:
                if f"mese {month}" in line:
                    match = re.search(r'(\d+\.\d+)', line)
                    if match:
                        avg = float(match.group(1))
                        if avg > 1.10:
                            scores['cycle'] = 0.2
                        elif avg < 1.08:
                            scores['cycle'] = -0.2
                        else:
                            scores['cycle'] = 0.0
                        break
            else:
                scores['cycle'] = 0.0
    except:
        scores['cycle'] = 0.0
    
    # Volumi
    try:
        with open('/home/carlo/AI_Trading/volume_context.txt', 'r') as f:
            text = f.read()
            import re
            match = re.search(r'Punteggio:\s*([-+]?\d+\.?\d*)', text)
            if match:
                scores['volume'] = float(match.group(1))
            else:
                scores['volume'] = 0.0
    except:
        scores['volume'] = 0.0
    
    # Esperienza (memoria errori)
    try:
        with open('/home/carlo/AI_Trading/experiences.json', 'r') as f:
            exp = json.load(f)
            recent = [e for e in exp if e.get('esito') == 'PERDITA'][-3:]
            if len(recent) >= 3:
                scores['experience'] = -0.2
            else:
                scores['experience'] = 0.0
    except:
        scores['experience'] = 0.0
    
    # Pesi
    weights = {
        'news': 0.2,
        'social': 0.2,
        'cycle': 0.15,
        'volume': 0.25,
        'experience': 0.2
    }
    
    # Calcola media ponderata
    total = 0.0
    weight_sum = 0.0
    for key in scores:
        total += scores[key] * weights[key]
        weight_sum += weights[key]
    
    final_score = total / weight_sum if weight_sum > 0 else 0.0
    print(f"Punteggio combinato: {final_score:.3f}", flush=True)
    
    # Soglie
    if final_score > 0.2:
        return "BUY"
    elif final_score < -0.2:
        return "SELL"
    else:
        return "HOLD"

def check_time_stop():
    try:
        with open(ORDERS_JSON) as f:
            orders = json.load(f)
        open_orders = [o for o in orders if o.get('status') == 'open']
        if not open_orders:
            return
        order = open_orders[0]
        ticket = order.get('ticket')
        if not ticket:
            return
        try:
            with open(OPEN_TIME_FILE) as f:
                open_times = json.load(f)
            open_time = open_times.get(str(ticket))
            if not open_time:
                open_times[str(ticket)] = time.time()
                with open(OPEN_TIME_FILE, "w") as f:
                    json.dump(open_times, f)
                return
            open_dt = datetime.fromtimestamp(open_time)
            if datetime.now() - open_dt > timedelta(hours=24):
                print(f"Operazione {ticket} aperta da più di 24h. Invio chiusura.", flush=True)
                cmd_path = os.path.join(MT4_FILES, "AI_BRIDGE_CMD.txt")
                with open(cmd_path, "w") as f:
                    f.write(f"CLOSE {ticket}\n")
                del open_times[str(ticket)]
                with open(OPEN_TIME_FILE, "w") as f:
                    json.dump(open_times, f)
        except Exception as e:
            print(f"Errore timestamp: {e}")
    except Exception as e:
        print(f"Errore time-stop: {e}")

def main():
    config = load_config()
    session = config.get("session", "all")
    print(f"Orchestratore avviato. Sessione: {session}", flush=True)
    while True:
        # Controllo Time-Stop
        check_time_stop()
        
        if not is_trading_hours(session):
            print(f"Fuori orario. UTC: {datetime.now(timezone.utc).hour}", flush=True)
            time.sleep(600)
            continue
        
        open_count = count_open_orders()
        if open_count >= MAX_OPEN_ORDERS:
            print("Limite operazioni raggiunto.", flush=True)
            time.sleep(600)
            continue
        
        signal = get_signal()
        print(f"Segnale AI: {signal}", flush=True)
        
        if signal in ("BUY", "SELL"):
            action = "buy" if signal == "BUY" else "sell"
            
            # Calcola ATR per SL/TP dinamici
            try:
                df = yf.download("EURUSD=X", period="1d", interval="15m", progress=False)
                df['ATR'] = df['High'].rolling(14).max() - df['Low'].rolling(14).min()
                atr = df['ATR'].iloc[-1]
                sl_distance = atr * 1.0   # 1x ATR
                tp_distance = atr * 1.5   # 1.5x ATR
                price = df['Close'].iloc[-1]
                if signal == "BUY":
                    sl = price - sl_distance
                    tp = price + tp_distance
                else:
                    sl = price + sl_distance
                    tp = price - tp_distance
                sl = round(sl, 5)
                tp = round(tp, 5)
                cmd = f"{action} 0.01 {sl} {tp}"
                print(f"Ordine {action} inviato con SL={sl} TP={tp}", flush=True)
            except Exception as e:
                print(f"Errore calcolo ATR, uso default: {e}", flush=True)
                cmd = action
            
            cmd_path = os.path.join(MT4_FILES, "AI_BRIDGE_CMD.txt")
            with open(cmd_path, "w") as f:
                f.write(f"{cmd}\n")
        else:
            print("HOLD", flush=True)
        
        time.sleep(600)

if __name__ == "__main__":
    main()
