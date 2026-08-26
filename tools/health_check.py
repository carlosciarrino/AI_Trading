import subprocess, json, logging, time, requests, os
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def send_telegram(text):
    try:
        token = "8928323847:AAGpoYGzlnAN39q-VM0O4ZlgrbLFXLiEzwk"
        chat_id = open(os.path.expanduser("~/.telegram_chat_id")).read().strip()
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={'chat_id': chat_id, 'text': text}, timeout=5)
    except:
        pass

def check_tmux(session_name="ai_workforce"):
    result = subprocess.run(["tmux", "list-sessions"], capture_output=True, text=True)
    if session_name in result.stdout:
        return True, "✅ Orchestratore attivo"
    else:
        return False, "❌ Orchestratore non in esecuzione"

def check_yahoo():
    try:
        import yfinance as yf
        df = yf.download("EURUSD=X", period="1d", interval="1d", multi_level_index=False)
        if df.empty:
            return False, "❌ Yahoo Finance: nessun dato"
        return True, f"✅ Yahoo Finance OK (prezzo {df['Close'].iloc[-1]:.5f})"
    except Exception as e:
        return False, f"❌ Yahoo Finance errore: {e}"

def check_ollama():
    try:
        resp = requests.post("http://localhost:11434/api/generate",
                             json={"model": "tinyllama", "prompt": "Ciao", "stream": False},
                             timeout=30)
        if resp.status_code == 200 and resp.json().get("response"):
            return True, "✅ Ollama OK"
        return False, "❌ Ollama risposta vuota"
    except Exception as e:
        return False, f"❌ Ollama errore: {e}"

def check_bridge():
    try:
        from core.mt4_bridge import MT4Bridge
        bridge = MT4Bridge()
        bridge.connect()
        bridge.disconnect()
        return True, "✅ Bridge MT4 OK"
    except Exception as e:
        return False, f"❌ Bridge MT4 errore: {e}"

def check_dashboard():
    try:
        r = requests.get("http://localhost:5000", timeout=5)
        if r.status_code == 200:
            return True, "✅ Dashboard OK"
        return False, f"❌ Dashboard errore {r.status_code}"
    except:
        return False, "❌ Dashboard non raggiungibile"

def main():
    logger.info("🔍 Avvio health check...")
    checks = [
        check_tmux(),
        check_yahoo(),
        check_ollama(),
        check_bridge(),
        check_dashboard()
    ]
    all_ok = True
    report = ["📊 *Report Health Check*"]
    for label, (ok, msg) in zip(["Orchestratore", "Yahoo", "Ollama", "Bridge", "Dashboard"], checks):
        report.append(f"{'🟢' if ok else '🔴'} {label}: {msg}")
        if not ok:
            all_ok = False

    report_text = "\n".join(report)
    logger.info(report_text)

    if not all_ok:
        send_telegram(f"⚠️ *ALLARME*: Health Check fallito\n{report_text}")
    else:
        send_telegram(f"✅ *Health Check OK*\n{report_text}")

    # Salva report su file
    with open("~/health_check.log", "w") as f:
        f.write(f"{datetime.now()}\n{report_text}\n\n")

if __name__ == "__main__":
    main()
