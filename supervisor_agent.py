#!/usr/bin/env python3
"""
Supervisor Agent - v4 (P001 + Financial Guard, 2026-10-30)
Legge stato agenti con ps. Controlla PNL giornaliero e drawdown.
Se i limiti finanziari vengono superati, KILLA l'orchestratore (blocco di sicurezza).
Aggiorna audit_status.json e scrive ALERT.md in caso di blocco.
"""
import os
import json
import subprocess
import time
from datetime import datetime, timezone

BASE = os.path.expanduser("~/AI_Trading")
AUDIT_JSON = os.path.join(BASE, "audit_status.json")
RESTART_LOG = os.path.join(BASE, "restart_log.json")
ALERT_MD = os.path.join(BASE, "docs", "ALERT.md")
ACCOUNT_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/account.json"
ORDERS_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/orders.json"
INTERVAL = 300

PY = "/home/carlo/AI_Trading_Agents/venv/bin/python3"

# Limiti finanziari (stringenti per salvaguardare il capitale)
MAX_DAILY_LOSS_PCT = 3.0    # Se perdita giornaliera > 3%, BLOCCA
MAX_DRAWDOWN_PCT = 8.0      # Se drawdown totale > 8%, BLOCCA
INITIAL_BALANCE = 100000.0  # Balance iniziale di riferimento (demo)

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
    script = SCRIPTS.get(name)
    if not script:
        return False
    try:
        r = subprocess.run(["ps", "-eo", "comm,args"], capture_output=True, text=True, timeout=5)
        if r.returncode != 0:
            return False
        for line in r.stdout.splitlines():
            parts = line.strip().split(None, 1)
            if len(parts) < 2:
                continue
            if parts[0] in ("python3", "python") and script in parts[1]:
                return True
        return False
    except Exception:
        return False


def agent_status():
    return {name: "active" if agent_alive(name) else "stopped" for name in SCRIPTS}


def read_account():
    try:
        with open(ACCOUNT_JSON) as f:
            return json.load(f)
    except Exception:
        return {"balance": 0, "equity": 0}


def check_financial_limits():
    """Ritorna (ok, reason) basato su PNL giornaliero, drawdown e perdite consecutive."""
    # Regola 1: 3 perdite consecutive
    ok, reason = check_consecutive_losses()
    if not ok:
        return False, reason

    # Regola 2: Drawdown e PNL giornaliero
    acc = read_account()
    balance = acc.get("balance", 0)
    equity = acc.get("equity", 0)

    if balance <= 0 or equity <= 0:
        return True, ""

    # Drawdown totale rispetto al balance iniziale
    drawdown_pct = ((INITIAL_BALANCE - equity) / INITIAL_BALANCE) * 100.0
    if drawdown_pct >= MAX_DRAWDOWN_PCT:
        return False, f"drawdown {drawdown_pct:.2f}% >= {MAX_DRAWDOWN_PCT}%"

    # PNL giornaliero (semplificato: equity vs balance)
    daily_loss_pct = ((balance - equity) / balance) * 100.0
    if daily_loss_pct >= MAX_DAILY_LOSS_PCT:
        return False, f"perdita giornaliera {daily_loss_pct:.2f}% >= {MAX_DAILY_LOSS_PCT}%"

    return True, ""


def check_consecutive_losses():
    """Ritorna (ok, reason) se ci sono 3 o piu' perdite consecutive."""
    try:
        with open(ORDERS_JSON) as f:
            orders = json.load(f)
        closed = [o for o in orders if o.get("status") == "closed"]
        if len(closed) < 3:
            return True, ""
        
        recent = closed[-3:]
        if all(float(o.get("pnl", 0)) < 0 for o in recent):
            return False, "3 operazioni consecutive chiuse in perdita"
    except Exception as e:
        log(f"Errore check_consecutive_losses: {e}")
    return True, ""


def kill_orchestrator():
    try:
        subprocess.run(["tmux", "kill-session", "-t", "ai_workforce"], capture_output=True, timeout=5)
        log("[KILL] Orchestratore bloccato dal supervisore per limiti finanziari.")
        return True
    except Exception as e:
        log(f"[ERRORE] kill_orchestrator: {e}")
        return False


def generate_diagnosis():
    """Analizza gli ultimi ordini per capire la causa delle perdite."""
    try:
        with open(ORDERS_JSON) as f:
            orders = json.load(f)
        closed = [o for o in orders if o.get("status") == "closed"]
        recent = closed[-5:] if len(closed) >= 5 else closed
        
        buys = sum(1 for o in recent if o.get("action") == "buy")
        sells = sum(1 for o in recent if o.get("action") == "sell")
        losses = sum(1 for o in recent if float(o.get("pnl", 0)) < 0)
        
        diag = []
        if buys == len(recent):
            diag.append("Il sistema ha aperto solo BUY. Verifica se il trend era effettivamente rialzista.")
        if sells == len(recent):
            diag.append("Il sistema ha aperto solo SELL. Verifica se il trend era effettivamente ribassista.")
        if losses == len(recent):
            diag.append("Tutte le ultime operazioni sono in perdita. La strategia e' contro-trend o i filtri non funzionano.")
            
        # Controlla il trend attuale
        try:
            with open('/home/carlo/AI_Trading/technical_context.txt') as f:
                tech = f.read().lower()
                if 'bear=true' in tech and buys > 0:
                    diag.append("ATTENZIONE: Trend BEAR rilevato ma il sistema ha aperto BUY. Il filtro P055 non ha bloccato.")
                if 'bull=true' in tech and sells > 0:
                    diag.append("ATTENZIONE: Trend BULL rilevato ma il sistema ha aperto SELL. Il filtro P055 non ha bloccato.")
        except Exception:
            pass

        if not diag:
            diag.append("Nessun pattern evidente nei log. Analizzare manualmente.")
        return "\n".join(f"- {d}" for d in diag)
    except Exception as e:
        return f"- Errore durante la diagnosi: {e}"

def write_alert(reason):
    ts = datetime.now().isoformat()
    diagnosis = generate_diagnosis()
    with open(ALERT_MD, "w") as f:
        f.write(f"# ALLARME SUPERVISORE ({ts})\n\n")
        f.write(f"Il supervisore ha bloccato l'orchestratore.\n")
        f.write(f"**Motivo:** {reason}\n\n")
        f.write(f"## Diagnosi Automatica\n{diagnosis}\n\n")
        f.write("## Azioni richieste:\n")
        f.write("1. Verificare il conto e le operazioni aperte.\n")
        f.write("2. Leggere la diagnosi sopra.\n")
        f.write("3. Correggere la strategia.\n")
        f.write("4. Riavviare manualmente: `tmux new-session -d -s ai_workforce '...'`\n")
        f.write("5. Rimuovere questo file dopo aver risolto.\n")


def write_audit(status, fin_ok, fin_reason):
    acc = read_account()
    audit = {
        "timestamp": datetime.now().isoformat(),
        "agents": status,
        "critical": {c: status.get(c, "stopped") for c in CRITICAL},
        "has_issue": any(status.get(c) == "stopped" for c in CRITICAL) or not fin_ok,
        "financial": {
            "balance": acc.get("balance", 0),
            "equity": acc.get("equity", 0),
            "ok": fin_ok,
            "reason": fin_reason,
        },
    }
    try:
        with open(AUDIT_JSON, "w") as f:
            json.dump(audit, f, indent=2)
    except Exception as e:
        log(f"ERRORE write_audit: {e}")


def restart_agent(agent, reason="stopped"):
    cmd = START_COMMANDS.get(agent)
    if not cmd:
        return False
    try:
        subprocess.run(["tmux", "kill-session", "-t", agent], capture_output=True, timeout=5)
    except Exception:
        pass
    try:
        subprocess.run(cmd, shell=True, timeout=15)
        log(f"Riavvio {agent} (motivo: {reason})")
        return True
    except Exception as e:
        log(f"ERRORE restart {agent}: {e}")
        return False


def main():
    log("Supervisor agent v4 (P001 + Financial Guard) avviato. Intervallo: " + str(INTERVAL) + "s")
    while True:
        try:
            status = agent_status()
            fin_ok, fin_reason = check_financial_limits()

            if not fin_ok:
                log(f"[ALERT] Limite finanziario superato: {fin_reason}")
                kill_orchestrator()
                write_alert(fin_reason)
                # Non riavviare l'orchestratore. Il supervisore resta in attesa.
                status["ai_workforce"] = "blocked_by_risk"

            write_audit(status, fin_ok, fin_reason)

            if fin_ok:
                to_restart = [c for c in CRITICAL if status.get(c) == "stopped"]
                if to_restart:
                    log(f"Critici fermi: {', '.join(to_restart)}")
                    for agent in to_restart:
                        restart_agent(agent, reason="stopped")
                else:
                    log("Tutti i critici attivi. Nessuna azione.")
            else:
                log("Orchestratore BLOCCATO. In attesa di intervento manuale.")

        except Exception as e:
            log(f"ERRORE nel ciclo principale: {e}")
        try:
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            log("Interrotto manualmente. Uscita.")
            break


if __name__ == "__main__":
    main()
