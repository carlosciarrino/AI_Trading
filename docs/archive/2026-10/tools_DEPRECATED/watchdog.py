import os, time, subprocess, json, logging, requests
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def send_telegram(text):
    token = "8928323847:AAGpoYGzlnAN39q-VM0O4ZlgrbLFXLiEzwk"
    # Il chat_id verrà impostato automaticamente dal bot
    try:
        # Leggi chat_id da file salvato dal bot
        chat_file = os.path.expanduser("~/.telegram_chat_id")
        if os.path.exists(chat_file):
            with open(chat_file) as f:
                chat_id = f.read().strip()
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, json={'chat_id': chat_id, 'text': text}, timeout=5)
    except:
        pass

def check_orchestrator():
    # 1. Controlla se il processo è in esecuzione
    result = subprocess.run(["tmux", "list-sessions"], capture_output=True, text=True)
    if "ai_workforce" not in result.stdout:
        logger.error("❌ Orchestratore non in esecuzione")
        send_telegram("⛔ ALLARME: Orchestratore non in esecuzione. Riavvio...")
        subprocess.run(["tmux", "new-session", "-d", "-s", "ai_workforce",
                       "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && while true; do python3 orchestrator.py 2>&1 | tee -a ~/orchestrator.log; sleep 3600; done"])
        return False

    # 2. Controlla il log (ultime 50 righe)
    log_file = "/home/carlo/orchestrator.log"
    if not os.path.exists(log_file):
        logger.error("❌ Log non trovato")
        return False

    with open(log_file) as f:
        lines = f.readlines()[-50:]
        text = "".join(lines)

    # 3. Verifica che ci siano prezzi reali (non 1.00000)
    if "Segnale: HOLD @ 1.00000" in text or "Segnale: BUY @ 1.00000" in text or "Segnale: SELL @ 1.00000" in text:
        logger.error("❌ Prezzi fittizi rilevati (1.00000)")
        send_telegram("⛔ ALLARME: Prezzi fittizi rilevati. Sistema in pausa.")
        subprocess.run(["tmux", "kill-session", "-t", "ai_workforce"])
        return False

    # 4. Verifica che non ci siano errori critici
    if "Error" in text or "Exception" in text or "Timeout" in text:
        last_errors = [line for line in lines if "Error" in line or "Exception" in line]
        logger.warning(f"⚠️ Errori rilevati: {len(last_errors)}")
        if len(last_errors) > 5:
            logger.error("❌ Troppi errori. Sistema in pausa.")
            send_telegram("⛔ ALLARME: Troppi errori. Sistema in pausa.")
            subprocess.run(["tmux", "kill-session", "-t", "ai_workforce"])
            return False

    return True

def main():
    logger.info("Watchdog avviato. Controllo ogni 5 minuti...")
    while True:
        check_orchestrator()
        time.sleep(300)

if __name__ == "__main__":
    main()
