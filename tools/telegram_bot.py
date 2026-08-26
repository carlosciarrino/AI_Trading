import sys, os
sys.path.insert(0, '/home/carlo/AI_Trading')
import json, time, requests, logging
from datetime import datetime
from tools.live_data import get_recent
from tools.support_resistance import find_sr

TOKEN = "8928323847:AAGpoYGzlnAN39q-VM0O4ZlgrbLFXLiEzwk"
CHAT_ID = None
URL = f"https://api.telegram.org/bot{TOKEN}"

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def send_message(text):
    if not TOKEN:
        return
    try:
        resp = requests.post(f"{URL}/sendMessage", json={'chat_id': CHAT_ID, 'text': text})
        return resp.json()
    except Exception as e:
        logger.error(f"Errore invio: {e}")

def get_updates(offset=None):
    url = f"{URL}/getUpdates"
    if offset:
        url += f"?offset={offset}"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get('result', [])
    except Exception as e:
        logger.error(f"Errore getUpdates: {e}")
        return []

def handle_commands():
    global CHAT_ID
    offset = None
    while True:
        updates = get_updates(offset)
        for u in updates:
            offset = u['update_id'] + 1
            msg = u.get('message', {})
            chat = msg.get('chat', {})
            text = msg.get('text', '')
            if not CHAT_ID:
                with open(os.path.expanduser("~/.telegram_chat_id"), "w") as f:
                    f.write(str(chat["id"]))
                CHAT_ID = chat.get('id')
                send_message("✅ Bot connesso. Comandi: /status, /start, /stop, /orders, /config, /set, /sr")
            if chat.get('id') != CHAT_ID:
                continue

            if text == '/status':
                send_message("✅ Sistema attivo. " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            elif text == '/stop':
                os.system("tmux kill-session -t ai_workforce 2>/dev/null")
                send_message("⛔ Orchestratore fermato.")
            elif text == '/start':
                os.system("cd /home/carlo/AI_Trading && tmux new-session -d -s ai_workforce 'bash -c \"source ~/AI_Trading_Agents/venv/bin/activate && while true; do python3 orchestrator.py; sleep 3600; done\"'")
                send_message("▶️ Orchestratore avviato.")
            elif text == '/orders':
                try:
                    with open(os.path.expanduser('~/mt4_shared/orders.json')) as f:
                        orders = json.load(f)
                    last = orders[-3:] if orders else []
                    send_message(str(last)[:500] if last else "Nessun ordine.")
                except:
                    send_message("Nessun ordine.")
            elif text == '/config':
                try:
                    with open('/home/carlo/AI_Trading/config.json') as f:
                        cfg = json.load(f)
                    send_message(f"Config: {cfg}")
                except:
                    send_message("Config non trovato.")
            elif text == '/sr':
                try:
                    df = get_recent("EUR/USD", interval="15min", length=50)
                    levels = find_sr(df)
                    send_message(f"📊 Livelli SR: {', '.join([f'{l:.5f}' for l in levels])}")
                except Exception as e:
                    send_message(f"❌ Errore SR: {e}")
            elif text.startswith('/set'):
                try:
                    parts = text.split()[1].split('=')
                    key, value = parts[0], parts[1]
                    with open('/home/carlo/AI_Trading/config.json') as f:
                        cfg = json.load(f)
                    cfg[key] = value
                    with open('/home/carlo/AI_Trading/config.json', 'w') as f:
                        json.dump(cfg, f, indent=2)
                    send_message(f"✅ Config aggiornata: {key}={value}")
                except Exception as e:
                    send_message(f"❌ Errore: {e}. Usa: /set timeframe=H1")
            else:
                send_message("Comandi: /status, /start, /stop, /orders, /config, /set, /sr")
        time.sleep(2)

if __name__ == '__main__':
    send_message("🤖 AI_BRIDGE Bot avviato.")
    handle_commands()
