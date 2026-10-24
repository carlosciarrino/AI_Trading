#!/usr/bin/env python3
"""
Supervisor Agent - v3-bis (P001, 2026-10-24)
Legge stato agenti con ps -eo comm,args: cerca python3 <script>.py.
Esclude il wrapper bash. Riavvia i critici morti. Aggiorna audit_status.json.

P001 fix: pane_current_command non e' affidabile (riporta il wrapper bash,
non il python3 figlio). pgrep -f matcha anche il wrapper (il testo del
comando bash -c contiene 'python3 ... script.py'). Usiamo ps e filtriamo
per comm == python3/python, args contiene script.py.
scouting_agent gira via cron, non in tmux: escluso dal check.
"""
import os
import json
import subprocess
import time
from datetime import datetime

BASE = os.path.expanduser("~/AI_Trading")
AUDIT_JSON = os.path.join(BASE, "audit_status.json")
RESTART_LOG = os.path.join(BASE, "restart_log.json")
INTERVAL = 300

PY = "/home/carlo/AI_Trading_Agents/venv/bin/python3"

SCRIPTS = {
    "ai_workforce": "orchestrator.py",
    "supervisor": "supervisor_agent.py",
    "news_agent": "news_agent.py",
    "social_agent": "social_agent.py",
    "cycle_agent": "cycle_agent.py",
    "volume_agent": "volume_agent.py",
    "experience_agent": "experience_agent.py",
    "kronos_agent": "kronos_agent.py",
    "nzt_agent": "nzt_agent.py",
    "market_anomaly": "market_anomaly_agent.py",
    "signal_observer": "signal_observer_agent.py",
    "strategy_validator": "strategy_validator.py",
    "reflection_agent": "reflection_agent.py",
    "technical_agent": "technical_agent.py",
}

AGENTS = {name: name for name in SCRIPTS}
CRITICAL = ["ai_workforce", "news_agent", "social_agent", "cycle_agent"]

START_COMMANDS = {
    "ai_workforce":     f"tmux new-session -d -s ai_workforce 'cd /home/carlo/AI_Trading && {PY} orchestrator.py > /home/carlo/ai_workforce.log 2>&1'",
    "supervisor":       f"tmux new-session -d -s supervisor 'cd /home/carlo/AI_Trading && {PY} supervisor_agent.py > /home/carlo/supervisor.log 2>&1'",
    "news_agent":       f"tmux new-session -d -s news_agent 'cd /home/carlo/AI_Trading && {PY} news_agent.py > /home/carlo/news_agent.log 2>&1'",
    "social_agent":     f"tmux new-session -d -s social_agent 'cd /home/carlo/AI_Trading && {PY} social_agent.py > /home/carlo/social_agent.log 2>&1'",
    "cycle_agent":      f"tmux new-session -d -s cycle_agent 'cd /home/carlo/AI_Trading && {PY} cycle_agent.py > /home/carlo/cycle_agent.log 2>&1'",
    "volume_agent":     f"tmux new-session -d -s volume_agent 'cd /home/carlo/AI_Trading && {PY} volume_agent.py > /home/carlo/volume_agent.log 2>&1'",
    "experience_agent": f"tmux new-session -d -s experience_agent 'cd /home/carlo/AI_Trading && {PY} experience_agent.py > /home/carlo/experience_agent.log 2>&1'",
    "kronos_agent":     f"tmux new-session -d -s kronos_agent 'cd /home/carlo/AI_Trading && {PY} kronos_agent.py > /home/carlo/kronos_agent.log 2>&1'",
    "nzt_agent":        f"tmux new-session -d -s nzt_agent 'cd /home/carlo/AI_Trading && {PY} nzt_agent.py > /home/carlo/nzt_agent.log 2>&1'",
    "market_anomaly":   f"tmux new-session -d -s market_anomaly 'cd /home/carlo/AI_Trading && {PY} market_anomaly_agent.py > /home/carlo/market_anomaly.log 2>&1'",
    "signal_observer":  f"tmux new-session -d -s signal_observer 'cd /home/carlo/AI_Trading && {PY} signal_observer_agent.py > /home/carlo/signal_observer.log 2>&1'",
    "strategy_validator": f"tmux new-session -d -s strategy_validator 'cd /home/carlo/AI_Trading && {PY} strategy_validator.py > /home/carlo/strategy_validator.log 2>&1'",
    "reflection_agent": f"tmux new-session -d -s reflection_agent 'cd /home/carlo/AI_Trading && {PY} reflection_agent.py > /home/carlo/reflection_agent.log 2>&1'",
    "technical_agent":  f"tmux new-session -d -s technical_agent 'cd /home/carlo/AI_Trading && {PY} technical_agent.py > /home/carlo/technical_agent.log 2>&1'",
}


def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{ts}] {msg}", flush=True)


def agent_alive(name):
    """True se esiste un processo python3/python con args contenente <script>.py.
    Esclude il wrapper bash (comm=bash, args='bash -c ... python3 ...')."""
    script = SCRIPTS.get(name)
    if not script:
        return False
    try:
        r = subprocess.run(
            ["ps", "-eo", "comm,args"],
            capture_output=True, text=True, timeout=5
        )
        if r.returncode != 0:
            return False
        for line in r.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            if len(parts) < 2:
                continue
            comm, args = parts[0], parts[1]
            if comm in ("python3", "python") and script in args:
                return True
        return False
    except Exception as e:
        log(f"ERRORE ps {name}: {e}")
        return False


def agent_status():
    status = {}
    for name in SCRIPTS:
        status[name] = "active" if agent_alive(name) else "stopped"
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


def write_audit(status):
    audit = {
        "timestamp": datetime.now().isoformat(),
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


def restart_agent(agent, reason="stopped"):
    cmd = START_COMMANDS.get(agent)
    if not cmd:
        log(f"Nessun comando di start per {agent}")
        return False
    try:
        subprocess.run(["tmux", "kill-session", "-t", agent],
                       capture_output=True, timeout=5)
    except Exception:
        pass
    try:
        subprocess.run(cmd, shell=True, timeout=15)
        log(f"Riavvio {agent} (motivo: {reason})")
        log_restart(agent, reason=reason)
        return True
    except Exception as e:
        log(f"ERRORE restart {agent}: {e}")
        return False


def main():
    log("Supervisor agent v3-bis (P001 ps) avviato. Intervallo: " + str(INTERVAL) + "s")
    while True:
        try:
            status = agent_status()
            write_audit(status)
            to_restart = [c for c in CRITICAL if status.get(c) == "stopped"]
            if to_restart:
                log(f"Critici fermi: {', '.join(to_restart)}")
                for agent in to_restart:
                    restart_agent(agent, reason="stopped")
            else:
                log("Tutti i critici attivi. Nessuna azione.")
        except Exception as e:
            log(f"ERRORE nel ciclo principale: {e}")
        try:
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            log("Interrotto manualmente. Uscita.")
            break


if __name__ == "__main__":
    main()
