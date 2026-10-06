import os, json, subprocess, logging, time, requests
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

VERIFICATION_DIR = "/home/carlo/AI_Trading/docs/verification"
PROJECT_DIR = "/home/carlo/AI_Trading"
TELEGRAM_TOKEN = "8928323847:AAGpoYGzlnAN39q-VM0O4ZlgrbLFXLiEzwk"

WATCH_MAP = {
    "tools/position_manager.py": "tests/test_position_manager.py",
    "orchestrator.py": "tests/test_orchestrator.py",
    "web_app.py": "tests/test_dashboard.py",
}

def send_telegram(text):
    chat_file = os.path.expanduser("~/.telegram_chat_id")
    if not os.path.exists(chat_file):
        logger.warning("chat_id non trovato, skip Telegram")
        return
    with open(chat_file) as f:
        chat_id = f.read().strip()
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text[:4000]},
            timeout=10
        )
    except Exception as e:
        logger.error(f"Errore Telegram: {e}")

def run_test(test_file):
    if not os.path.exists(test_file):
        return False, f"Test file non trovato: {test_file}"
    try:
        result = subprocess.run(
            ["python3", test_file],
            cwd=PROJECT_DIR,
            capture_output=True, text=True, timeout=120
        )
        success = result.returncode == 0
        output = result.stdout + result.stderr
        return success, output
    except subprocess.TimeoutExpired:
        return False, "Timeout (120s)"
    except Exception as e:
        return False, str(e)

def verify_file(file_path):
    rel_path = os.path.relpath(file_path, PROJECT_DIR)
    test_file = WATCH_MAP.get(rel_path)
    
    if not test_file:
        logger.info(f"Nessun test mappato per {rel_path}, skip.")
        return None
    
    logger.info(f"Eseguo test per {rel_path}: {test_file}")
    success, output = run_test(test_file)
    
    os.makedirs(VERIFICATION_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = os.path.join(VERIFICATION_DIR, f"{timestamp}_{rel_path.replace('/', '_')}.md")
    
    with open(report_file, "w") as f:
        f.write(f"# Verifica {rel_path}\n\n")
        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Esito: {'✅ PASS' if success else '❌ FAIL'}\n\n")
        f.write(f"Test: `{test_file}`\n\n")
        f.write(f"## Output\n\n```\n{output}\n```\n")
    
    emoji = "✅" if success else "❌"
    msg = f"{emoji} *Verifica {rel_path}*\n"
    msg += f"Esito: {'PASS' if success else 'FAIL'}\n"
    msg += f"Test: {test_file}\n"
    if not success:
        msg += f"\nErrore:\n```\n{output[-500:]}\n```"
    send_telegram(msg)
    
    status_file = os.path.join(VERIFICATION_DIR, "last_status.json")
    status = {
        "file": rel_path,
        "test": test_file,
        "success": success,
        "timestamp": datetime.now().isoformat(),
        "output_tail": output[-500:]
    }
    with open(status_file, "w") as f:
        json.dump(status, f, indent=2)
    
    logger.info(f"Report salvato: {report_file}")
    return success

def main():
    logger.info("Verifier avviato. Monitoraggio ogni 60 secondi...")
    last_mtimes = {}

    while True:
        try:
            for rel_file in WATCH_MAP.keys():
                full_path = os.path.join(PROJECT_DIR, rel_file)
                if not os.path.exists(full_path):
                    continue
                mtime = os.path.getmtime(full_path)
                if rel_file in last_mtimes and last_mtimes[rel_file] != mtime:
                    logger.info(f"File modificato: {rel_file}")
                    verify_file(full_path)
                last_mtimes[rel_file] = mtime
        except Exception as e:
            logger.error(f"Errore: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
