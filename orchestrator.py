import yfinance as yf
import json, time, os, requests
from datetime import datetime, timezone

CONFIG_PATH = os.path.expanduser("~/AI_Trading/config.json")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"
MAX_OPEN_ORDERS = 1

# Orari di trading (UTC - 2 = ora italiana)
LONDRA_APERTURA = 8  # 8:00 UTC
LONDRA_CHIUSURA = 17
NEW_YORK_APERTURA = 13
NEW_YORK_CHIUSURA = 22
TOKYO_APERTURA = 0
TOKYO_CHIUSURA = 9

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def is_trading_hours():
    now_utc = datetime.now(timezone.utc).hour
    # Londra e New York sono le sessioni principali
    if LONDRA_APERTURA <= now_utc < LONDRA_CHIUSURA or NEW_YORK_APERTURA <= now_utc < NEW_YORK_CHIUSURA:
        return True
    return False

def count_open_orders():
    try:
        with open(os.path.expanduser('~/mt4_shared/orders.json')) as f:
            orders = json.load(f)
        return len([o for o in orders if o.get('status') == 'open'])
    except:
        return 0

def get_signal():
    prompt = f"Sei un analista finanziario. Dammi un segnale per EURUSD su timeframe 15min. Rispondi solo con: BUY, SELL o HOLD."
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False, "options": {"num_predict": 10}}, timeout=600)
        r.raise_for_status()
        signal = r.json()["response"].strip().upper()
        if "SOLD" in signal or "SELL" in signal: return "SELL"
        if "BOUGHT" in signal or "BUY" in signal: return "BUY"
        return "HOLD"
    except Exception as e:
        print(f"Errore AI: {e}")
        return "HOLD"

def main():
    print("Orchestratore avviato (con gestione orari)", flush=True)
    while True:
        # Se non è orario di trading, non fare nulla
        if not is_trading_hours():
            print(f"Fuori orario di trading. Attendo... (UTC: {datetime.now(timezone.utc).hour})", flush=True)
            time.sleep(600)  # Controlla ogni 10 minuti
            continue
        
        open_count = count_open_orders()
        if open_count >= MAX_OPEN_ORDERS:
            print("Limite operazioni raggiunto. Attendo...", flush=True)
            time.sleep(600)
            continue
        
        signal = get_signal()
        print(f"Segnale AI: {signal}", flush=True)
        
        if signal in ("BUY", "SELL"):
            action = "buy" if signal == "BUY" else "sell"
            # Invia ordine al bridge MT4 (placeholder)
            print(f"Ordine {action} inviato", flush=True)
        else:
            print("HOLD", flush=True)
        
        time.sleep(600)

if __name__ == "__main__":
    main()
