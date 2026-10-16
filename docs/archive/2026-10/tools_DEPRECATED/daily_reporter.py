import re, json, os, requests, logging
from datetime import datetime, timedelta
from collections import Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_creds():
    bot_file = "/home/carlo/AI_Trading/tools/telegram_bot.py"
    token = None
    if os.path.exists(bot_file):
        with open(bot_file) as f:
            content = f.read()
        match = re.search(r'TOKEN\s*=\s*"([^"]+)"', content)
        if match:
            token = match.group(1)
    chat_file = os.path.expanduser("~/.telegram_chat_id")
    chat_id = None
    if os.path.exists(chat_file):
        with open(chat_file) as f:
            chat_id = f.read().strip()
    return token, chat_id

def send_telegram(text):
    token, chat_id = get_creds()
    if not token or not chat_id:
        logger.error("Token o CHAT_ID non trovati. Invia un messaggio al bot e riprova.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={'chat_id': chat_id, 'text': text}, timeout=10)
    except Exception as e:
        logger.error(f"Errore invio: {e}")

def analyze_hold_logs():
    log_file = "/home/carlo/orchestrator.log"
    if not os.path.exists(log_file):
        return "Log non trovato."

    cutoff = datetime.now() - timedelta(hours=24)
    hold_entries = []
    with open(log_file) as f:
        for line in f:
            try:
                parts = line.split(",")
                if len(parts) < 2: continue
                ts = parts[0].strip()
                log_time = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                if log_time < cutoff: continue
                if "Segnale finale:" in line:
                    match = re.search(r"Segnale finale: (\w+)", line)
                    if match and match.group(1) == "HOLD":
                        reason = "Motivo sconosciuto"
                        if "rischio negato" in line.lower():
                            reason = "Risk Manager (drawdown/rischio)"
                        elif "supporto" in line.lower() or "resistenza" in line.lower():
                            reason = "Supporto/Resistenza vicino"
                        elif "AI" in line.lower() or "ollama" in line.lower():
                            reason = "AI ha deciso HOLD (nessuna opportunità)"
                        hold_entries.append(f"{log_time.strftime('%H:%M')} - {reason}")
            except:
                continue

    if not hold_entries:
        return "Nessun HOLD registrato nelle ultime 24 ore."

    counter = Counter([r.split(" - ")[1] for r in hold_entries])
    summary = "\n".join([f"- {k}: {v}" for k, v in counter.items()])

    report = f"""📊 *Report Giornaliero HOLD - {datetime.now().strftime('%d/%m/%Y')}*

Totale HOLD: {len(hold_entries)}
Motivi principali:
{summary}

Ultimi 5 HOLD:
{chr(10).join(hold_entries[-5:])}
"""
    return report

def main():
    report = analyze_hold_logs()
    send_telegram(report)
    logger.info("Report inviato.")

if __name__ == '__main__':
    main()
