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
        return len([o for o in orders if o.get('status') == 'open'])
    except:
        return 0

def get_signal():
    prompt = "Sei un analista finanziario. Dammi un segnale per EURUSD su timeframe 15min. Rispondi solo con: BUY, SELL o HOLD."
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False, "options": {"num_predict": 10}}, timeout=600)
        r.raise_for_status()
        signal = r.json()["response"].strip().upper()
        if "SOLD" in signal or "SELL" in signal:
            return "SELL"
        if "BOUGHT" in signal or "BUY" in signal:
            return "BUY"
        return "HOLD"
    except Exception as e:
        print(f"Errore AI: {e}")
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
        check_time_stop()
        if not is_trading_hours(session):
            print(f"Fuori orario. UTC: {datetime.now(timezone.utc).hour}", flush=True)
            time.sleep(600)
            continue
        if count_open_orders() >= MAX_OPEN_ORDERS:
            print("Limite operazioni raggiunto.", flush=True)
            time.sleep(600)
            continue
        signal = get_signal()
        print(f"Segnale AI: {signal}", flush=True)
        if signal in ("BUY", "SELL"):
            action = "buy" if signal == "BUY" else "sell"
            with open(os.path.join(MT4_FILES, "AI_BRIDGE_CMD.txt"), "w") as f:
                f.write(f"{action}\n")
            print(f"Ordine {action} inviato", flush=True)
        else:
            print("HOLD", flush=True)
        time.sleep(600)

if __name__ == "__main__":
    main()
