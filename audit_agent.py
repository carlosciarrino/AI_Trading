#!/usr/bin/env python3
import os
import subprocess
import json
import time
from datetime import datetime

BASE = os.path.expanduser("~/AI_Trading")
REPORT_FILE = os.path.join(BASE, "audit_report.txt")
ORDERS_FILE = os.path.expanduser("~/mt4_shared/orders.json")

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
            status[f] = f"ok (età {age:.1f}h)"
        else:
            status[f] = "mancante"
    return status

def run_audit():
    lines = []
    lines.append(f"=== AUDIT REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # Tmux
    sessions = check_tmux()
    lines.append("\n[TMUX SESSIONS]")
    lines.append(sessions if sessions else "Nessuna sessione attiva")
    
    # Ordini
    orders = check_orders()
    lines.append(f"\n[ORDINI] Aperti: {orders['open']}, Chiusi: {orders['closed']}")
    if orders['last']:
        lines.append(f"Ultimo ordine: {orders['last']}")
    
    # Report
    lines.append("\n[REPORT]")
    for f, st in check_reports().items():
        lines.append(f"  {f}: {st}")
    
    # Verifica agenti critici
    critical = ["ai_workforce", "news_agent", "social_agent", "cycle_agent"]
    lines.append("\n[AGENTI CRITICI]")
    for a in critical:
        if a in sessions:
            lines.append(f"  {a}: ATTIVO")
        else:
            lines.append(f"  {a}: ⚠️ FERMO")
    
    # Scrive report
    report = "\n".join(lines)
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    print(report)
    return report

if __name__ == "__main__":
    run_audit()
