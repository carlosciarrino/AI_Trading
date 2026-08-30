#!/usr/bin/env python3
import os
import json
import subprocess
import time
from datetime import datetime

BASE = os.path.expanduser("~/AI_Trading")
AUDIT_JSON = os.path.join(BASE, "audit_status.json")
LOG_FILE = os.path.join(BASE, "restart_log.json")
INTERVAL = 300  # 5 secondi per test, poi 300

# Comandi di avvio per gli agenti critici (presi da web_app.py)
START_COMMANDS = {
    "ai_workforce": "tmux new-session -d -s ai_workforce 'cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents_py311/bin/activate && python3 orchestrator.py'",
    "news_agent": "tmux new-session -d -s news_agent 'cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents_py311/bin/activate && python3 news_agent.py'",
    "social_agent": "tmux new-session -d -s social_agent 'cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents_py311/bin/activate && python3 social_agent.py'",
    "cycle_agent": "tmux new-session -d -s cycle_agent 'cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents_py311/bin/activate && python3 cycle_agent.py'"
}
def load_audit():
    try:
        with open(AUDIT_JSON) as f:
            return json.load(f)
    except:
        return {}

def log_restart(agent, reason="stopped"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "reason": reason,
        "action": "restart"
    }
    try:
        with open(LOG_FILE, "r") as f:
            log = json.load(f)
    except:
        log = []
    log.append(entry)
    # mantieni solo ultimi 1000 eventi
    if len(log) > 1000:
        log = log[-1000:]
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def restart_agent(agent):
    cmd = START_COMMANDS.get(agent)
    if not cmd:
        return
    subprocess.run(cmd, shell=True)
    print(f"[{datetime.now()}] Riavvio {agent}")
    log_restart(agent)

def main():
    print("Supervisor agent avviato. Controllo ogni 5 minuti.")
    while True:
        audit = load_audit()
        critical = audit.get("critical", {})
        for agent, status in critical.items():
            if status == "stopped":
                restart_agent(agent)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

