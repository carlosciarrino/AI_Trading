import os, time, json, subprocess
from datetime import datetime

ORDERS_PATH = os.path.expanduser("~/mt4_shared/orders.json")
LOG_PATH = "/home/carlo/orchestrator.log"

MAX_WAIT_FOR_LOG_UPDATE = 1200
MAX_ORDERS = 1

def get_file_mod_time(path):
    try:
        return os.path.getmtime(path)
    except:
        return None

def check_process_activity(process_name):
    output = subprocess.run(["pgrep", "-f", process_name], capture_output=True, text=True)
    return bool(output.stdout.strip())

def main():
    print("Sentinella Avanzata attiva. Monitoro processo E produttività...")
    
    while True:
        # 1. Se il processo è morto
        if not check_process_activity("orchestrator.py"):
            print("⚠️ ORCHESTRATOR MORTO! Fermo tutto.")
            os.system("tmux kill-session -t ai_workforce 2>/dev/null")
            break
            
        # 2. Se il processo è vivo ma non scrive sul log
        current_log_time = get_file_mod_time(LOG_PATH)
        if current_log_time is not None:
            if time.time() - current_log_time > MAX_WAIT_FOR_LOG_UPDATE:
                print("⚠️ ORCHESTRATOR BLOCCATO! Nessun aggiornamento log da troppo tempo. Fermo tutto.")
                os.system("tmux kill-session -t ai_workforce 2>/dev/null")
                break
        
        # 3. Se ci sono troppi ordini aperti
        try:
            with open(ORDERS_PATH, "r") as f:
                orders = json.load(f)
            open_orders = [o for o in orders if o.get("status") == "open"]
            if len(open_orders) > MAX_ORDERS:
                print(f"⚠️ TROPPI ORDINI APERTI ({len(open_orders)}). Fermo tutto.")
                os.system("tmux kill-session -t ai_workforce 2>/dev/null")
                break
        except:
            pass
            
        time.sleep(30)

if __name__ == "__main__":
    main()
