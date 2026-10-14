#!/usr/bin/env python3
"""
Supervisor Agent - v2
Riscritto 2026-10-14.
Legge stato agenti da tmux, riavvia i critici fermi, aggiorna audit_status.json.
"""
import os
import json
import subprocess
from datetime import datetime

BASE = os.path.expanduser("~/AI_Trading")
AUDIT_JSON = os.path.join(BASE, "audit_status.json")
RESTART_LOG = os.path.join(BASE, "restart_log.json")
INTERVAL = 300  # secondi tra cicli (5 minuti)

AGENTS = {
    "ai_workforce": "Orchestratore principale",
    "cycle_agent": "Cicli storici",
    "experience_agent": "Memoria errori",
    "kronos_agent": "Timing",
    "market_anomaly": "Anomalie mercato",
    "news_agent": "Notizie macro",
    "nzt_agent": "Strategia NZT",
    "signal_observer": "Osserva segnali",
    "social_agent": "Sentiment social",
    "strategy_validator": "Valida strategie",
    "supervisor": "Supervisione",
    "volume_agent": "Volumi",
}

CRITICAL = ["ai_workforce", "news_agent", "social_agent", "cycle_agent"]

VENV = "/home/carlo/AI_Trading_Agents/venv/bin/activate"

START_COMMANDS = {
    "ai_workforce": f"tmux new-session -d -s ai_workforce 'cd /home/carlo/AI_Trading && source {VENV} && python3 orchestrator.py'",
    "news_agent": f"tmux new-session -d -s news_agent 'cd /home/carlo/AI_Trading && source {VENV} && python3 news_agent.py'",
    "social_agent": f"tmux new-session -d -s social_agent 'cd /home/carlo/AI_Trading && source {VENV} && python3 social_agent.py'",
    "cycle_agent": f"tmux new-session -d -s cycle_agent 'cd /home/carlo/AI_Trading && source {VENV} && python3 cycle_agent.py'",
}
def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{ts}] {msg}", flush=True)


def tmux_sessions():
    try:
        out = subprocess.run(
            ["tmux", "ls"],
            capture_output=True, text=True, timeout=5
        )
        if out.returncode != 0:
            return []
        sessions = []
        for line in out.stdout.splitlines():
            name = line.split(":")[0].strip()
            if name:
                sessions.append(name)
        return sessions
    except Exception as e:
        log(f"ERRORE tmux_sessions: {e}")
        return []


def agent_status(sessions):
    status = {}
    for name in AGENTS:
        status[name] = "active" if name in sessions else "stopped"
    return status


def read_orders_summary():
    orders_path = "/home/carlo/Scrivania/XM MT4/MQL4/Files/orders.json"
    try:
        with open(orders_path) as f:
            orders = json.load(f)
        if not isinstance(orders, list):
            return {"open": 0, "closed": 0, "last": None}
        open_n = sum(1 for o in orders if o.get("status") == "open")
        closed_n = sum(1 for o in orders if o.get("status") == "closed")
        last = orders[-1] if orders else None
        return {"open": open_n, "closed": closed_n, "last": last}
    except Exception:
        return {"open": 0, "closed": 0, "last": None}


def write_audit(sessions, status):
    audit = {
        "timestamp": datetime.now().isoformat(),
        "sessions": "\n".join(f"{s}: 1 windows" for s in sessions) + "\n" if sessions else "",
        "orders": read_orders_summary(),
        "agents": status,
        "critical": {c: status.get(c, "stopped") for c in CRITICAL},
        "has_issue": any(status.get(c) == "stopped" for c in CRITICAL),
    }
    try:
        with open(AUDIT_JSON, "w") as f:
            json.dump(audit, f, indent=2)
    except Exception as e:
        log(f"ERRORE write_audit: {e}")


def log_restart(agent, reason="stopped"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "reason": reason,
        "action": "restart",
    }
    try:
        with open(RESTART_LOG) as f:
            log_data = json.load(f)
        if not isinstance(log_data, list):
            log_data = []
    except Exception:
        log_data = []
    log_data.append(entry)
    if len(log_data) > 1000:
        log_data = log_data[-1000:]
    try:
        with open(RESTART_LOG, "w") as f:
            json.dump(log_data, f, indent=2)
    except Exception as e:
        log(f"ERRORE log_restart: {e}")


def restart_agent(agent):
    cmd = START_COMMANDS.get(agent)
    if not cmd:
        log(f"Nessun comando di start per {agent}")
        return False
    try:
        subprocess.run(cmd, shell=True, timeout=15)
        log(f"Riavvio {agent}")
        log_restart(agent)
        return True
    except Exception as e:
        log(f"ERRORE restart {agent}: {e}")
        return False
def main():
    log("Supervisor agent v2 avviato. Intervallo: " + str(INTERVAL) + "s")
    while True:
        try:
            sessions = tmux_sessions()
            status = agent_status(sessions)
            write_audit(sessions, status)

            stopped_critical = [c for c in CRITICAL if status.get(c) == "stopped"]
            if stopped_critical:
                log(f"Critici fermi: {', '.join(stopped_critical)}")
                for agent in stopped_critical:
                    restart_agent(agent)
            else:
                log("Tutti i critici attivi. Nessuna azione.")

        except Exception as e:
            log(f"ERRORE nel ciclo principale: {e}")

        try:
            import time
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            log("Interrotto manualmente. Uscita.")
            break


if __name__ == "__main__":
    main()
