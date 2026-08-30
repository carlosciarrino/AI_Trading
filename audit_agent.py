#!/usr/bin/env python3
import os
import subprocess
import json
import time
from datetime import datetime

BASE = os.path.expanduser("~/AI_Trading")
REPORT_FILE = os.path.join(BASE, "audit_report.txt")
JSON_REPORT = os.path.join(BASE, "audit_status.json")
ORDERS_FILE = os.path.expanduser("~/mt4_shared/orders.json")

CRITICAL_AGENTS = ["ai_workforce", "news_agent", "social_agent", "cycle_agent"]

def check_tmux():
    out = subprocess.run(["tmux", "ls"], capture_output=True, text=True)
    sessions = out.stdout if out.returncode == 0 else ""
    return sessions

def check_orders():
    try:
        with open(ORDERS_FILE) as f:
            orders = json.load(f)
        open_orders = [o for o in orders if o.get('status') == 'open']
        closed_orders = [o for o in orders if o.get('status') == 'closed']
        return {"open": len(open_orders), "closed": len(closed_orders), "last": orders[-1] if orders else None}
    except:
        return {"open": 0, "closed": 0, "last": None}

def check_reports():
    files = ["report_strategia.txt", "report_video.txt", "report_multivideo.txt", "youtube_context.txt", "news_context.txt"]
    status = {}
    for f in files:
        path = os.path.join(BASE, f)
        if os.path.exists(path):
            mtime = os.path.getmtime(path)
            age = (time.time() - mtime) / 3600
            status[f] = f"ok ({age:.1f}h)"
        else:
            status[f] = "mancante"
    return status

def run_audit():
    sessions = check_tmux()
    orders = check_orders()
    reports = check_reports()

    # Verifica agenti critici
    critical_status = {}
    for a in CRITICAL_AGENTS:
        critical_status[a] = "active" if a in sessions else "stopped"

    # Determina se c'è un problema
    has_issue = any(v == "stopped" for v in critical_status.values()) or orders["open"] > 0

    # Costruisci report JSON
    data = {
        "timestamp": datetime.now().isoformat(),
        "sessions": sessions,
        "orders": orders,
        "reports": reports,
        "critical": critical_status,
        "has_issue": has_issue,
        "critical_agents": CRITICAL_AGENTS
    }

    with open(JSON_REPORT, "w") as f:
        json.dump(data, f, indent=2)

    # Testo leggibile
    lines = []
    lines.append(f"=== AUDIT REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    lines.append("\n[TMUX SESSIONS]")
    lines.append(sessions if sessions else "Nessuna sessione attiva")
    lines.append(f"\n[ORDINI] Aperti: {orders['open']}, Chiusi: {orders['closed']}")
    if orders['last']:
        lines.append(f"Ultimo ordine: {orders['last']}")
    lines.append("\n[REPORT]")
    for f, st in reports.items():
        lines.append(f"  {f}: {st}")
    lines.append("\n[AGENTI CRITICI]")
    for a, st in critical_status.items():
        icon = "✅" if st == "active" else "⚠️"
        lines.append(f"  {a}: {icon} {st.upper()}")

    report_text = "\n".join(lines)
    with open(REPORT_FILE, "w") as f:
        f.write(report_text)
    print(report_text)
    return data

if __name__ == "__main__":
    run_audit()
