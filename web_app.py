#!/usr/bin/env python3
"""
AI_BRIDGE Dashboard - web_app.py
Versione unificata 2026-10-14
Legge account.json e orders.json da MT4, mostra stato agenti tmux.
"""
from flask import Flask, render_template_string, jsonify, request
import json
import os
import subprocess
from datetime import datetime, timedelta

app = Flask(__name__)

# =====================
# PATH FILES MT4
# =====================
MT4_FILES = "/home/carlo/Scrivania/XM MT4/MQL4/Files"
ACCOUNT_JSON = os.path.join(MT4_FILES, "account.json")
ORDERS_JSON  = os.path.join(MT4_FILES, "orders.json")
AUDIT_JSON   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audit_status.json")

# =====================
# AGENTI TMUX
# =====================
AGENTS = {
    "cycle_agent":         "Analizza cicli storici e stagionalita' del mercato.",
    "experience_agent":    "Impara dagli errori passati e aggiorna la memoria.",
    "kronos_agent":        "Analisi temporale e timing operativo.",
    "market_anomaly":      "Rileva anomalie di mercato.",
    "news_agent":          "Analizza notizie macro.",
    "nzt_agent":           "Strategia NZT.",
    "signal_observer":     "Osserva e valida segnali.",
    "social_agent":        "Sentiment da social e news trending.",
    "strategy_validator":  "Valida strategie su dati storici.",
    "supervisor":          "Supervisiona l'orchestrazione degli agenti.",
    "volume_agent":        "Analisi volumi.",
}

# =====================
# HELPER: LETTURA FILE MT4
# =====================
def read_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None

def read_audit():
    return read_json(AUDIT_JSON)
BASE_HTML = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} · AI_BRIDGE</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', system-ui, sans-serif; background: #0b0e14; color: #e5e9f0; display: flex; min-height: 100vh; }
        .sidebar { width: 240px; background: #131722; border-right: 1px solid #2a2e39; padding: 24px 16px; display: flex; flex-direction: column; flex-shrink: 0; height: 100vh; position: sticky; top: 0; }
        .sidebar .logo { font-size: 20px; font-weight: 700; margin-bottom: 32px; display: flex; align-items: center; gap: 10px; }
        .sidebar .logo span { background: linear-gradient(135deg, #2962ff, #7c3aed); padding: 6px 10px; border-radius: 8px; font-size: 14px; }
        .sidebar nav a { color: #78828c; text-decoration: none; padding: 10px 14px; border-radius: 8px; font-size: 14px; font-weight: 500; display: block; cursor: pointer; margin-bottom: 4px; }
        .sidebar nav a:hover { background: #2a2e39; color: #e5e9f0; }
        .sidebar .footer { margin-top: auto; font-size: 12px; color: #4a5568; border-top: 1px solid #2a2e39; padding-top: 16px; }
        .main { flex: 1; padding: 24px 32px; overflow-y: auto; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .header h1 { font-size: 24px; font-weight: 600; }
        .header .status { display: flex; align-items: center; gap: 12px; background: #1e222d; padding: 8px 18px; border-radius: 40px; font-size: 14px; }
        .header .status .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
        .header .status .dot.online { background: #00c853; }
        .header .status .dot.offline { background: #ff1744; }
        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 28px; }
        .kpi-card { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 16px 20px; }
        .kpi-card .label { font-size: 13px; color: #78828c; text-transform: uppercase; }
        .kpi-card .value { font-size: 24px; font-weight: 700; margin-top: 4px; }
        .kpi-card .value.green { color: #00c853; }
        .kpi-card .value.red { color: #ff1744; }
        .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        .card-project { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 24px; cursor: pointer; transition: all 0.2s; }
        .card-project:hover { border-color: #2962ff; transform: translateY(-2px); }
        .card-project h3 { font-size: 18px; margin-bottom: 8px; }
        .card-project .desc { font-size: 13px; color: #78828c; margin-bottom: 12px; }
        .card-project .stat { font-size: 14px; color: #00c853; font-weight: 600; }
        .card-project .stat.offline { color: #ff1744; }
        .controls { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 28px; }
        .controls button { border: none; padding: 10px 24px; border-radius: 40px; font-weight: 600; font-size: 14px; cursor: pointer; }
        .controls .start { background: #00c853; color: #0b0e14; }
        .controls .stop { background: #ff1744; color: #fff; }
        .controls .restart { background: #2962ff; color: #fff; }
        .link-btn { display: inline-block; background: #2962ff; color: #fff; padding: 10px 24px; border-radius: 40px; text-decoration: none; font-weight: 600; font-size: 14px; margin-bottom: 20px; }
        .link-btn:hover { background: #1e4fd6; }
        .table-wrap { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 16px 20px; margin-bottom: 28px; overflow-x: auto; }
        .table-wrap h3 { font-size: 16px; font-weight: 600; margin-bottom: 12px; }
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        th { text-align: left; padding: 10px 8px; color: #78828c; border-bottom: 1px solid #2a2e39; }
        td { padding: 10px 8px; border-bottom: 1px solid #1e222d; }
        .buy { color: #00c853; font-weight: 600; }
        .sell { color: #ff1744; font-weight: 600; }
        .placeholder { background: #131722; border: 1px dashed #2a2e39; border-radius: 12px; padding: 40px; text-align: center; color: #78828c; }
        .agent-row button { border: none; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; cursor: pointer; margin-right: 4px; }
        .agent-row .btn-start { background: #00c853; color: #0b0e14; }
        .agent-row .btn-stop { background: #ff1744; color: #fff; }
        .agent-row .btn-restart { background: #2962ff; color: #fff; }
        .agent-status { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
        .agent-status.active { background: #0d3d1e; color: #00c853; }
        .agent-status.stopped { background: #3d0d0d; color: #ff1744; }
        @media (max-width: 768px) { .sidebar { display: none; } .main { padding: 16px; } }
    </style>
</head>
<body>
<div class="sidebar">
    <div class="logo"><span>▲</span> AI_BRIDGE</div>
    <nav>
        <a href="/">🏠 Home</a>
        <a href="/trading">💱 Trading</a>
        <a href="/agents">🤖 Agenti</a>
        <a href="/verifier">✅ Verifier</a>
        <a href="/media">🎬 Media</a>
        <a href="/ecommerce">🛒 E-commerce</a>
    </nav>
    <div class="footer">v4.0 · {{ now }}</div>
</div>
<div class="main">
    <div class="header">
        <h1>{{ title }}</h1>
        <div class="status"><span class="dot online"></span><span>Online</span><span style="color:#4a5568;">|</span><span>{{ now }}</span></div>
    </div>
    {{ content | safe }}
</div>
</body>
</html>
"""

def render_page(title, content):
    return render_template_string(
        BASE_HTML,
        title=title,
        content=content,
        now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
# =====================
# HELPER TMUX
# =====================
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
    except Exception:
        return []

def agent_status():
    sessions = tmux_sessions()
    status = {}
    for name in AGENTS:
        status[name] = "active" if name in sessions else "stopped"
    return status

# =====================
# HELPER PNL
# =====================
def calculate_pnl(period):
    orders = read_json(ORDERS_JSON) or []
    if not isinstance(orders, list):
        return 0.0
    now = datetime.now()
    if period == "day":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        return 0.0
    total = 0.0
    for o in orders:
        if o.get("status") != "closed":
            continue
        ts = o.get("close_time") or o.get("time") or 0
        try:
            dt = datetime.fromtimestamp(int(ts))
        except Exception:
            continue
        if dt >= start:
            try:
                total += float(o.get("pnl") or 0)
            except Exception:
                pass
    return total

# =====================
# ROUTE: HOME
# =====================
@app.route('/')
def index():
    sessions = tmux_sessions()
    trading_on = "ai_workforce" in sessions
    agents_on = any(a in sessions for a in AGENTS)
    content = f"""
    <div class="card-grid">
        <div class="card-project" onclick="location.href='/trading'">
            <h3>💱 Forex Trading</h3>
            <div class="desc">Stato conto, ordini aperti, PNL giorno/settimana</div>
            <div class="stat {'online' if trading_on else 'offline'}">{'● Attivo' if trading_on else '● Fermo'}</div>
        </div>
        <div class="card-project" onclick="location.href='/agents'">
            <h3>🤖 Agenti</h3>
            <div class="desc">Controllo agenti tmux: attiva, ferma, riavvia</div>
            <div class="stat {'online' if agents_on else 'offline'}">{'● Attivi' if agents_on else '● Fermi'}</div>
        </div>
        <div class="card-project" onclick="location.href='/verifier'">
            <h3>✅ Verifier</h3>
            <div class="desc">Test automatici post-modifica</div>
            <div class="stat">● Vedi stato</div>
        </div>
        <div class="card-project" onclick="location.href='/media'">
            <h3>🎬 Media Company</h3>
            <div class="desc">Generazione video automatica</div>
            <div class="stat offline">● Pianificato</div>
        </div>
    </div>
    """
    return render_page("🏠 Home", content)
# =====================
# ROUTE: TRADING
# =====================
@app.route('/trading')
def trading():
    # --- Inizio Financial Guard ---
    audit = read_audit()
    audit_color = "green"
    audit_label = "OK"
    alert_banner = ""
    if audit and not audit.get("financial", {}).get("ok", True):
        audit_color = "red"
        audit_label = "BLOCCATO"
        alert_banner = f'<div style="background:#ff1744;color:white;padding:12px;border-radius:8px;margin-bottom:20px;font-weight:bold;">⚠️ ALLARME: {audit["financial"].get("reason", "Motivo sconosciuto")}. Controlla ALERT.md</div>'
    elif audit and audit.get("has_issue", False):
        audit_color = "red"
        audit_label = "ATTENZIONE"
        alert_banner = '<div style="background:#ff9100;color:white;padding:12px;border-radius:8px;margin-bottom:20px;font-weight:bold;">⚠️ Attenzione: agenti critici fermi o problemi rilevati.</div>'
    # --- Fine Financial Guard ---

    account = read_json(ACCOUNT_JSON) or {}
    orders = read_json(ORDERS_JSON) or []
    if not isinstance(orders, list):
        orders = []

    balance     = float(account.get("balance", 0) or 0)
    equity      = float(account.get("equity", 0) or 0)
    margin      = float(account.get("margin", 0) or 0)
    free_margin = float(account.get("free_margin", 0) or 0)
    profit      = float(account.get("profit", 0) or 0)
    currency    = account.get("currency", "EUR")
    login       = account.get("login", "N/D")
    server      = account.get("server", "N/D")
    ts          = account.get("timestamp", 0)
    ts_str      = datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S') if ts else "N/D"

    pnl_day  = calculate_pnl("day")
    pnl_week = calculate_pnl("week")

    open_orders   = [o for o in orders if o.get("status") == "open"]
    closed_orders = [o for o in orders if o.get("status") == "closed"]
    closed_orders = sorted(closed_orders, key=lambda o: o.get("time", 0), reverse=True)[:20]

    def color(v):
        return "green" if v >= 0 else "red"

    rows_open = ""
    if open_orders:
        for o in open_orders:
            rows_open += (
                f"<tr>"
                f"<td>{o.get('ticket','')}</td>"
                f"<td class='{o.get('action','')}'>{o.get('action','')}</td>"
                f"<td>{o.get('lots','')}</td>"
                f"<td>{o.get('price','')}</td>"
                f"<td>{o.get('sl','')}</td>"
                f"<td>{o.get('tp','')}</td>"
                f"<td>{o.get('pnl',0)}</td>"
                f"</tr>"
            )
    else:
        rows_open = "<tr><td colspan='7' style='text-align:center;color:#4a5568;'>Nessuna operazione aperta</td></tr>"

    rows_closed = ""
    if closed_orders:
        for o in closed_orders:
            try:
                pnl_v = float(o.get('pnl') or 0)
            except Exception:
                pnl_v = 0
            clr = "green" if pnl_v >= 0 else "red"
            rows_closed += (
                f"<tr>"
                f"<td>{o.get('ticket','')}</td>"
                f"<td class='{o.get('action','')}'>{o.get('action','')}</td>"
                f"<td>{o.get('lots','')}</td>"
                f"<td>{o.get('price','')}</td>"
                f"<td>{o.get('close_price','')}</td>"
                f"<td class='{clr}'>{pnl_v:+.2f}</td>"
                f"</tr>"
            )
    else:
        rows_closed = "<tr><td colspan='6' style='text-align:center;color:#4a5568;'>Nessuna operazione chiusa</td></tr>"

    content = f"""
    <a class="link-btn" href="https://www.tradingview.com/chart/?symbol=FX:EURUSD" target="_blank" rel="noopener">📈 Apri TradingView</a>

    <div class="kpi-grid">
        <div class="kpi-card"><div class="label">Saldo</div><div class="value">{balance:,.2f} {currency}</div></div>
        <div class="kpi-card"><div class="label">Equity</div><div class="value">{equity:,.2f} {currency}</div></div>
        <div class="kpi-card"><div class="label">Margin</div><div class="value">{margin:,.2f}</div></div>
        <div class="kpi-card"><div class="label">Free Margin</div><div class="value">{free_margin:,.2f}</div></div>
        <div class="kpi-card"><div class="label">Profit flottante</div><div class="value {color(profit)}">{profit:+,.2f}</div></div>
        <div class="kpi-card"><div class="label">PNL oggi</div><div class="value {color(pnl_day)}">{pnl_day:+,.2f}</div></div>
        <div class="kpi-card"><div class="label">PNL settimana</div><div class="value {color(pnl_week)}">{pnl_week:+,.2f}</div></div>
        <div class="kpi-card"><div class="label">Conto</div><div class="value" style="font-size:14px;">{login} · {server}</div></div>
    </div>

    <div style="color:#78828c;font-size:12px;margin-bottom:20px;">Ultimo aggiornamento account.json: {ts_str}</div>

    <div class="table-wrap">
        <h3>📋 Operazioni Aperte ({len(open_orders)})</h3>
        <table>
            <tr><th>Ticket</th><th>Azione</th><th>Lotti</th><th>Prezzo</th><th>SL</th><th>TP</th><th>PNL</th></tr>
            {rows_open}
        </table>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card"><div class="label">Salute Sistema (Supervisore)</div><div class="value {audit_color}">{audit_label}</div></div>
    </div>
    {alert_banner}

    <div class="table-wrap">
        <h3>📜 Operazioni Chiuse (ultime 20)</h3>
        <table>
            <tr><th>Ticket</th><th>Azione</th><th>Lotti</th><th>Apertura</th><th>Chiusura</th><th>PNL</th></tr>
            {rows_closed}
        </table>
    </div>
    """
    return render_page("💱 Trading", content)
# =====================
# ROUTE: AGENTS
# =====================
@app.route('/agents')
def agents():
    status = agent_status()
    rows = ""
    for name, desc in AGENTS.items():
        st = status.get(name, "stopped")
        st_class = "active" if st == "active" else "stopped"
        st_label = "Attivo" if st == "active" else "Fermo"
        rows += (
            f"<tr class='agent-row'>"
            f"<td><strong>{name}</strong><br><span style='color:#78828c;font-size:12px;'>{desc}</span></td>"
            f"<td><span class='agent-status {st_class}'>{st_label}</span></td>"
            f"<td>"
            f"<button class='btn-start' onclick=\"agentAction('{name}','start')\">▶ Start</button>"
            f"<button class='btn-stop' onclick=\"agentAction('{name}','stop')\">⏹ Stop</button>"
            f"<button class='btn-restart' onclick=\"agentAction('{name}','restart')\">🔄 Restart</button>"
            f"</td>"
            f"</tr>"
        )

    content = f"""
    <div style="color:#78828c;font-size:12px;margin-bottom:16px;">
        Agenti tmux della sessione <strong>ai_workforce</strong>. Start / Stop / Restart agiscono sul singolo agente.
    </div>
    <div class="table-wrap">
        <h3>🤖 Agenti ({len(AGENTS)})</h3>
        <table>
            <tr><th>Agente</th><th>Stato</th><th>Azioni</th></tr>
            {rows}
        </table>
    </div>
    <script>
    function agentAction(name, action) {{
        if (!confirm(action.toUpperCase() + ' ' + name + '?')) return;
        fetch('/api/agent/' + name + '/' + action, {{method: 'POST'}})
            .then(r => r.json())
            .then(d => {{
                alert(d.message || d.error || 'Fatto');
                location.reload();
            }})
            .catch(e => alert('Errore: ' + e));
    }}
    </script>
    """
    return render_page("🤖 Agenti", content)

# =====================
# API: CONTROLLO AGENTE
# =====================
@app.route('/api/agent/<name>/<action>', methods=['POST'])
def api_agent(name, action):
    if name not in AGENTS:
        return jsonify({"error": f"Agente '{name}' sconosciuto"}), 404
    if action not in ("start", "stop", "restart"):
        return jsonify({"error": f"Azione '{action}' non valida"}), 400

    sessions = tmux_sessions()
    is_active = name in sessions

    try:
        if action == "start":
            if is_active:
                return jsonify({"message": f"{name} gia' attivo"})
            script = f"/home/carlo/AI_Trading/{name}.py"
            if not os.path.exists(script):
                return jsonify({"error": f"Script {script} non trovato"}), 404
            cmd = f"tmux new-session -d -s {name} 'cd /home/carlo/AI_Trading && python3 {name}.py'"
            subprocess.run(cmd, shell=True, timeout=10)
            return jsonify({"message": f"{name} avviato"})

        elif action == "stop":
            if not is_active:
                return jsonify({"message": f"{name} gia' fermo"})
            subprocess.run(f"tmux kill-session -t {name}", shell=True, timeout=10)
            return jsonify({"message": f"{name} fermato"})

        elif action == "restart":
            subprocess.run(f"tmux kill-session -t {name}", shell=True, timeout=10)
            script = f"/home/carlo/AI_Trading/{name}.py"
            if not os.path.exists(script):
                return jsonify({"error": f"Script {script} non trovato"}), 404
            cmd = f"tmux new-session -d -s {name} 'cd /home/carlo/AI_Trading && python3 {name}.py'"
            subprocess.run(cmd, shell=True, timeout=10)
            return jsonify({"message": f"{name} riavviato"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# =====================
# ROUTE: VERIFIER
# =====================
@app.route('/verifier')
def verifier():
    status = {}
    status_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'docs', 'verification', 'last_status.json'
    )
    try:
        with open(status_file) as f:
            status = json.load(f)
    except Exception:
        pass

    ok = bool(status.get("success"))
    ok_color = "#00c853" if ok else "#ff1744"
    ok_label = "PASS" if ok else ("FAIL" if status else "N/D")
    ts = status.get("timestamp", "N/D")
    if ts and ts != "N/D":
        ts = ts[:19]

    content = f"""
    <div class="kpi-grid">
        <div class="kpi-card"><div class="label">Ultimo File</div><div class="value" style="font-size:16px;">{status.get('file', 'N/D')}</div></div>
        <div class="kpi-card"><div class="label">Esito</div><div class="value" style="color:{ok_color};">{ok_label}</div></div>
        <div class="kpi-card"><div class="label">Timestamp</div><div class="value" style="font-size:14px;">{ts}</div></div>
    </div>
    <div class="table-wrap">
        <h3>📋 Output Ultimo Test</h3>
        <pre style="background:#0b0e14;padding:12px;border-radius:8px;color:#78828c;font-size:12px;white-space:pre-wrap;overflow-x:auto;">{status.get('output_tail', 'Nessun output')}</pre>
    </div>
    """
    return render_page("✅ Verifier", content)

# =====================
# ROUTE: MEDIA
# =====================
@app.route('/media')
def media():
    content = """
    <div class="kpi-grid">
        <div class="kpi-card"><div class="label">Video Oggi</div><div class="value">0</div></div>
        <div class="kpi-card"><div class="label">Video Settimana</div><div class="value">0</div></div>
        <div class="kpi-card"><div class="label">Visualizzazioni</div><div class="value">0</div></div>
        <div class="kpi-card"><div class="label">Revenue</div><div class="value">$0.00</div></div>
    </div>
    <div class="table-wrap">
        <h3>🎬 Video Prodotti</h3>
        <div class="placeholder">Agenti Media non ancora attivi. Progetto pianificato.</div>
    </div>
    """
    return render_page("🎬 Media Company", content)

# =====================
# ROUTE: ECOMMERCE
# =====================
@app.route('/ecommerce')
def ecommerce():
    content = """
    <div class="placeholder">
        <h3>🛒 E-commerce</h3>
        <p>Progetto pianificato. Da avviare dopo Media Company.</p>
    </div>
    """
    return render_page("🛒 E-commerce", content)
# =====================
# API: ACCOUNT
# =====================
@app.route('/api/account')
def api_account():
    account = read_json(ACCOUNT_JSON)
    if not account:
        return jsonify({"error": "account.json non trovato o non leggibile"}), 404
    return jsonify(account)

# =====================
# API: ORDERS
# =====================
@app.route('/api/orders')
def api_orders():
    orders = read_json(ORDERS_JSON)
    if orders is None:
        return jsonify({"error": "orders.json non trovato o non leggibile"}), 404
    if not isinstance(orders, list):
        return jsonify({"error": "orders.json non e' una lista"}), 500
    seen = set()
    dedup = []
    for o in orders:
        t = o.get("ticket")
        if t in seen:
            continue
        seen.add(t)
        dedup.append(o)
    return jsonify(dedup)

# =====================
# API: PNL
# =====================
@app.route('/api/pnl')
def api_pnl():
    period = request.args.get("period", "day")
    if period not in ("day", "week"):
        return jsonify({"error": "period deve essere 'day' o 'week'"}), 400
    return jsonify({"period": period, "pnl": calculate_pnl(period)})

# =====================
# MAIN
# =====================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
