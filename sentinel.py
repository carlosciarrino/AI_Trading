import os, time, json, signal, subprocess

ORDERS_PATH = os.path.expanduser("~/mt4_shared/orders.json")
LOG_PATH = "/home/carlo/orchestrator.log"
MAX_ORDERS = 1  # Limite massimo operazioni aperte

def get_open_orders():
    try:
        with open(ORDERS_PATH) as f:
            orders = json.load(f)
        return [o for o in orders if o.get("status") == "open"]
    except:
        return []

def check_process():
    output = subprocess.run(["pgrep", "-f", "orchestrator.py"], capture_output=True, text=True)
    return bool(output.stdout.strip())

def stop_everything():
    print("⚠️ SENTINELLA: ANOMALIA RILEVATA! STOP TOTALE DEL SISTEMA.")
    os.system("tmux kill-session -t ai_workforce 2>/dev/null")
    os.system("tmux kill-session -t dashboard 2>/dev/null")

def main():
    print("Sentinella attiva. Monitoro il sistema in tempo reale...")
    while True:
        open_orders = get_open_orders()
        if len(open_orders) > MAX_ORDERS:
            print(f"⚠️ TROPPE OPERAZIONI APERTE ({len(open_orders)}). FORZO LO STOP.")
            stop_everything()
            break
        
        if not check_process():
            print("⚠️ PROCESSO ORCHESTRATOR MORTO! FORZO LO STOP PER SICUREZZA.")
            stop_everything()
            break
        
        try:
            with open(LOG_PATH, "r") as f:
                log_content = f.read()[-5000:]
            if "Traceback" in log_content or "AttributeError" in log_content:
                print("⚠️ ERRORE NEL LOG! FORZO LO STOP.")
                stop_everything()
                break
        except:
            pass
        
        time.sleep(10)

if __name__ == "__main__":
    main()
