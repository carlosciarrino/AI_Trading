import yfinance as yf
import json, time, os, requests
from datetime import datetime

MT4_FILES_DIR = "/home/carlo/Scrivania/XM MT4/MQL4/Files"
CMD_FILE = os.path.join(MT4_FILES_DIR, "AI_BRIDGE_CMD.txt")
RES_FILE = os.path.join(MT4_FILES_DIR, "AI_BRIDGE_RES.txt")
ORDERS_PATH = os.path.expanduser("~/mt4_shared/orders.json")
CONFIG_PATH = os.path.expanduser("~/AI_Trading/config.json")
REPORT_PATH = os.path.expanduser("~/AI_Trading/AI_REPORT_GIORNALIERO.txt")

NEWS_PATH = os.path.expanduser("~/AI_Trading/news_context.txt")
SOCIAL_PATH = os.path.expanduser("~/AI_Trading/social_context.txt")
CYCLES_PATH = os.path.expanduser("~/AI_Trading/cycles_context.txt")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"
MAX_OPEN_ORDERS = 1

def load_config():
    with open(CONFIG_PATH) as f: return json.load(f)

def read_context_file(path):
    try:
        with open(path, "r") as f: return f.read()
    except: return ""

def count_open_orders():
    try:
        with open(ORDERS_PATH) as f: orders = json.load(f)
        return len([o for o in orders if o.get("status") == "open"])
    except: return 0

def warmup_model():
    print("Riscaldamento modello AI...", flush=True)
    try:
        requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": "ping", "stream": False}, timeout=300)
        print("Modello AI pronto.", flush=True)
    except Exception as e: print(f"Errore warm-up: {e}", flush=True)

def get_signal(symbol, timeframe, news, social, cycles):
    # L'AI ora ragiona su TUTTE le informazioni disponibili
    prompt = f"""Sei un analista finanziario. 
    Dati tecnici attuali di {symbol} (timeframe {timeframe}).
    Notizie macro: {news}
    Sentiment social: {social}
    Cicli storici stagionali: {cycles}
    Considera attentamente TUTTE le informazioni. 
    Se le notizie o i social sono fortemente negativi, scegli HOLD. 
    Rispondi SOLO con: BUY, SELL o HOLD."""
    
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False, "options": {"num_predict": 20}}, timeout=600)
        signal = response.json()["response"].strip().upper()
        if "SOLD" in signal or "SELL" in signal: return "SELL", prompt
        if "BOUGHT" in signal or "BUY" in signal: return "BUY", prompt
        return "HOLD", prompt
    except Exception as e:
        print(f"Errore AI: {e}", flush=True)
        return "HOLD", prompt

def write_report(prompt, signal, reason, price, sl, tp, status):
    try:
        with open(REPORT_PATH, "a") as f:
            f.write(f"\n=== REPORT AI - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.write(f"Decisione: {signal} | Motivo: {reason}\n")
            f.write(f"Prompt completo: {prompt}\n")
            f.write(f"Prezzo: {price} | SL: {sl} | TP: {tp} | Stato: {status}\n")
            f.write("-" * 50 + "\n")
    except: pass

def write_order_to_file(action, lots, price, sl, tp):
    cmd = f"{action},{lots},{price},{sl},{tp}"
    try:
        with open(CMD_FILE, "w") as f: f.write(cmd)
        print(f"Comando scritto per MT4: {cmd}", flush=True)
        return True
    except Exception as e: print(f"Errore scrittura: {e}", flush=True); return False

def wait_for_response(timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(RES_FILE):
            with open(RES_FILE, "r") as f: res = f.read().strip()
            os.remove(RES_FILE)
            return res
        time.sleep(0.5)
    return "ERR:TIMEOUT"

def update_orders_file(action, price, sl, tp, ticket):
    orders = []
    if os.path.exists(ORDERS_PATH):
        try:
            with open(ORDERS_PATH) as f: orders = json.load(f)
        except: orders = []
    orders = [o for o in orders if o.get("status") != "open"]
    order = {"action": action, "lots": 0.01, "price": price, "sl": sl, "tp": tp, "time": time.time(), "status": "open", "ticket": ticket, "pnl": 0}
    orders.append(order)
    with open(ORDERS_PATH, "w") as f: json.dump(orders, f, indent=2)

def main():
    config = load_config()
    symbol = "EURUSD=X"
    timeframe = config.get("timeframe", "15min")
    lot = config.get("lot", 0.01)
    
    warmup_model()
    print("Orchestrator avviato (con analisi News/Social/Cicli)", flush=True)

    while True:
        open_count = count_open_orders()
        print(f"Operazioni aperte: {open_count} (limite: {MAX_OPEN_ORDERS})", flush=True)

        if open_count >= MAX_OPEN_ORDERS:
            print("Limite raggiunto. Attendo chiusura...", flush=True)
            time.sleep(600); continue

        df = yf.download(symbol, period="1d", interval="1h", progress=False)
        if df.empty: time.sleep(60); continue

        news = read_context_file(NEWS_PATH)
        social = read_context_file(SOCIAL_PATH)
        cycles = read_context_file(CYCLES_PATH)

        signal, prompt = get_signal(symbol, timeframe, news, social, cycles)
        print(f"Segnale AI: {signal}", flush=True)

        price = float(df["Close"].iloc[-1])
        sl = price * 0.995
        tp = price * 1.005

        if signal in ("BUY", "SELL"):
            action = "buy" if signal == "BUY" else "sell"
            if write_order_to_file(action, lot, price, sl, tp):
                response = wait_for_response()
                if "OK:" in response:
                    ticket = response.split(":")[1]
                    update_orders_file(action, price, sl, tp, ticket)
                    write_report(prompt, signal, "Segnale confermato", price, sl, tp, "APERTO")
                else:
                    write_report(prompt, signal, f"Errore MT4: {response}", price, sl, tp, "ERRORE")
        else:
            write_report(prompt, signal, "AI ha deciso di non rischiare (HOLD)", price, sl, tp, "NESSUN ORDINE")

        time.sleep(600)

if __name__ == "__main__":
    main()
