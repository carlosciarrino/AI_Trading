from flask import Flask, render_template_string, jsonify, request
import json, os, yfinance as yf
from datetime import datetime

app = Flask(__name__)

# =====================
# TEMPLATE BASE
# =====================
BASE_HTML = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} · AI_BRIDGE</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #0b0e14; color: #e5e9f0; display: flex; min-height: 100vh; }
        .sidebar { width: 240px; background: #131722; border-right: 1px solid #2a2e39; padding: 24px 16px; display: flex; flex-direction: column; flex-shrink: 0; height: 100vh; position: sticky; top: 0; }
        .sidebar .logo { font-size: 20px; font-weight: 700; margin-bottom: 32px; display: flex; align-items: center; gap: 10px; }
        .sidebar .logo span { background: linear-gradient(135deg, #2962ff, #7c3aed); padding: 6px 10px; border-radius: 8px; font-size: 14px; }
        .sidebar nav a { color: #78828c; text-decoration: none; padding: 10px 14px; border-radius: 8px; font-size: 14px; font-weight: 500; display: block; cursor: pointer; margin-bottom: 4px; }
        .sidebar nav a:hover, .sidebar nav a.active { background: #2a2e39; color: #e5e9f0; }
        .sidebar .footer { margin-top: auto; font-size: 12px; color: #4a5568; border-top: 1px solid #2a2e39; padding-top: 16px; }
        .main { flex: 1; padding: 24px 32px; overflow-y: auto; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .header h1 { font-size: 24px; font-weight: 600; }
        .header .status { display: flex; align-items: center; gap: 12px; background: #1e222d; padding: 8px 18px; border-radius: 40px; font-size: 14px; }
        .header .status .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
        .header .status .dot.online { background: #00c853; }
        .header .status .dot.offline { background: #ff1744; }
        #verification-banner { margin-bottom: 20px; padding: 12px 20px; border-radius: 8px; display: none; font-size: 14px; }
        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 28px; }
        .kpi-card { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 16px 20px; }
        .kpi-card .label { font-size: 13px; color: #78828c; text-transform: uppercase; }
        .kpi-card .value { font-size: 24px; font-weight: 700; margin-top: 4px; }
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
        .section { display: none; margin-bottom: 28px; }
        .section.active { display: block; }
        .config-area { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 20px 24px; display: flex; flex-wrap: wrap; align-items: flex-end; gap: 16px; }
        .config-area label { font-size: 13px; color: #78828c; display: flex; flex-direction: column; gap: 4px; }
        .config-area select, .config-area input { background: #1e222d; border: 1px solid #2a2e39; border-radius: 8px; padding: 8px 14px; color: #e5e9f0; font-size: 14px; }
        .config-area .save-btn { background: #2962ff; border: none; border-radius: 40px; padding: 10px 24px; color: #fff; font-weight: 600; cursor: pointer; }
        .chart-container { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 16px 20px; margin-bottom: 28px; }
        .table-wrap { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 16px 20px; margin-bottom: 28px; overflow-x: auto; }
        .table-wrap h3 { font-size: 16px; font-weight: 600; margin-bottom: 12px; }
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        th { text-align: left; padding: 10px 8px; color: #78828c; border-bottom: 1px solid #2a2e39; }
        td { padding: 10px 8px; border-bottom: 1px solid #1e222d; }
        .buy { color: #00c853; font-weight: 600; }
        .sell { color: #ff1744; font-weight: 600; }
        .log-box { background: #0b0e14; border: 1px solid #2a2e39; border-radius: 12px; padding: 16px 20px; max-height: 200px; overflow-y: auto; font-family: monospace; font-size: 12px; color: #78828c; white-space: pre-wrap; }
        .placeholder { background: #131722; border: 1px dashed #2a2e39; border-radius: 12px; padding: 40px; text-align: center; color: #78828c; }
        @media (max-width: 768px) { .sidebar { display: none; } .main { padding: 16px; } }
    </style>
    <script src="https://cdn.plot.ly/plotly-2.27.1.min.js"></script>
</head>
<body>
<div class="sidebar">
    <div class="logo"><span>▲</span> AI_BRIDGE</div>
    <nav>
        <a href="/">🏠 Home</a>
        <a href="/trading">💱 Trading</a>
        <a href="/media">🎬 Media</a>
        <a href="/ecommerce">🛒 E-commerce</a>
        <a href="/verifier">✅ Verifier</a>
    </nav>
    <div class="footer">v3.0 · {{ now }}</div>
</div>
<div class="main">
    <div class="header">
        <h1>{{ title }}</h1>
        <div class="status"><span class="dot online" id="status_dot"></span><span id="status_text">Online</span><span style="color:#4a5568;">|</span><span>{{ now }}</span></div>
    </div>
    <div id="verification-banner">
        <strong>Stato Verifica:</strong> <span id="verification-text">Nessuna verifica recente</span>
    </div>
    {{ content | safe }}
</div>
<script>
function loadVerificationStatus() {
    fetch('/api/verification_status')
        .then(r => r.json())
        .then(data => {
            const banner = document.getElementById('verification-banner');
            const text = document.getElementById('verification-text');
            if (!data || !data.timestamp) { banner.style.display = 'none'; return; }
            banner.style.display = 'block';
            const date = new Date(data.timestamp).toLocaleString('it-IT');
            if (data.success) {
                banner.style.background = '#0d3d1e';
                banner.style.color = '#00c853';
                text.innerText = `✅ ${data.file} - PASS (${date})`;
            } else {
                banner.style.background = '#3d0d0d';
                banner.style.color = '#ff1744';
                text.innerText = `❌ ${data.file} - FAIL (${date})`;
            }
        }).catch(e => console.error(e));
}
setInterval(loadVerificationStatus, 30000);
loadVerificationStatus();
</script>
</body>
</html>
"""

def render_page(title, content):
    return render_template_string(BASE_HTML, title=title, content=content, now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.template_filter('timestamp')
def timestamp_filter(s):
    try:
        return datetime.fromtimestamp(int(s)).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(s)

# =====================
# HOME
# =====================
@app.route('/')
def index():
    projects_online = os.system("tmux list-sessions | grep -q ai_workforce") == 0
    verifier_online = os.system("tmux list-sessions | grep -q verifier") == 0
    content = f"""
    <div class="card-grid">
        <div class="card-project" onclick="location.href='/trading'">
            <h3>💱 Forex Trading</h3>
            <div class="desc">Azienda trading algoritmico con agenti AI, break-even, trailing stop</div>
            <div class="stat {'online' if projects_online else 'offline'}">{'● Attivo' if projects_online else '● Fermo'}</div>
        </div>
        <div class="card-project" onclick="location.href='/media'">
            <h3>🎬 Media Company</h3>
            <div class="desc">Generazione automatica video per YouTube, TikTok, Reels</div>
            <div class="stat offline">● Da avviare</div>
        </div>
        <div class="card-project" onclick="location.href='/ecommerce'">
            <h3>🛒 E-commerce</h3>
            <div class="desc">Dropshipping e affiliazione automatica</div>
            <div class="stat offline">● Pianificato</div>
        </div>
        <div class="card-project" onclick="location.href='/verifier'">
            <h3>✅ Verifier</h3>
            <div class="desc">Test automatici post-modifica</div>
            <div class="stat {'online' if verifier_online else 'offline'}">{'● Attivo' if verifier_online else '● Fermo'}</div>
        </div>
    </div>
    """
    return render_page("🏠 Home", content)

# =====================
# TRADING
# =====================
@app.route('/trading')
def trading():
    orders = []
    try:
        with open(os.path.expanduser('~/mt4_shared/orders.json')) as f:
            orders = json.load(f)
    except: pass
    open_orders = [o for o in orders if o.get('status') == 'open']
    content = f"""
    <div class="kpi-grid">
        <div class="kpi-card"><div class="label">Capitale</div><div class="value">100.000,00</div></div>
        <div class="kpi-card"><div class="label">Operazioni Aperte</div><div class="value">{len(open_orders)}</div></div>
        <div class="kpi-card"><div class="label">PNL Giorno</div><div class="value">+0,00</div></div>
        <div class="kpi-card"><div class="label">Drawdown Max</div><div class="value">0,00%</div></div>
    </div>
    <div class="controls">
        <button class="start" onclick="fetch('/api/command',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{cmd:'start'}})}}).then(r=>r.json()).then(d=>alert(d.message))">▶ Avvia</button>
        <button class="stop" onclick="fetch('/api/command',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{cmd:'stop'}})}}).then(r=>r.json()).then(d=>alert(d.message))">⏹ Ferma</button>
        <button class="restart" onclick="fetch('/api/command',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{cmd:'restart'}})}}).then(r=>r.json()).then(d=>alert(d.message))">🔄 Riavvia</button>
    </div>
    <div class="chart-container">
        <h3>📈 Grafico EUR/USD</h3>
        <div style="display:flex; gap:12px; margin-bottom:12px; flex-wrap:wrap;">
            <select id="chart_symbol" onchange="loadChart()">
                <option value="EURUSD=X" selected>EUR/USD</option>
                <option value="GBPUSD=X">GBP/USD</option>
                <option value="GC=F">XAU/USD</option>
            </select>
            <select id="chart_interval" onchange="loadChart()">
                <option value="1m">1 min</option>
                <option value="5m">5 min</option>
                <option value="15m" selected>15 min</option>
                <option value="1h">1 ora</option>
                <option value="4h">4 ore</option>
                <option value="1d">Daily</option>
            </select>
            <button onclick="loadChart()" style="background:#2962ff;border:none;border-radius:40px;padding:8px 20px;color:#fff;font-weight:600;cursor:pointer;">Aggiorna</button>
        </div>
        <div id="candlestick-chart" style="height:400px;"></div>
    </div>
    <div class="table-wrap">
        <h3>📋 Operazioni Aperte</h3>
        <table>
            <tr><th>Stato</th><th>Azione</th><th>Lotti</th><th>Prezzo</th><th>SL</th><th>TP</th><th>PNL</th></tr>
            {''.join([f"<tr><td>{o.get('status')}</td><td class='{o.get('action')}'>{o.get('action')}</td><td>{o.get('lots')}</td><td>{o.get('price')}</td><td>{o.get('sl')}</td><td>{o.get('tp')}</td><td>{o.get('pnl', 0)}</td></tr>" for o in open_orders]) if open_orders else '<tr><td colspan="7" style="text-align:center;color:#4a5568;">Nessuna operazione aperta</td></tr>'}
        </table>
    </div>
    <script>
    function loadChart() {{
        const symbol = document.getElementById('chart_symbol').value;
        const interval = document.getElementById('chart_interval').value;
        fetch('/api/chart_data', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify({{symbol: symbol, period: '30d', interval: interval}})
        }})
        .then(r => r.json())
        .then(data => {{
            if (data.error) {{
                document.getElementById('candlestick-chart').innerHTML = '<p style="color:#ff1744;">' + data.error + '</p>';
                return;
            }}
            const trace = {{
                x: data.map(d => d.Date),
                open: data.map(d => d.Open),
                high: data.map(d => d.High),
                low: data.map(d => d.Low),
                close: data.map(d => d.Close),
                type: 'candlestick',
                increasing: {{line: {{color: '#00c853'}}}},
                decreasing: {{line: {{color: '#ff1744'}}}}
            }};
            const layout = {{
                template: 'plotly_dark',
                xaxis: {{title: 'Data', type: 'date'}},
                yaxis: {{title: 'Prezzo'}},
                margin: {{l: 40, r: 20, t: 20, b: 40}},
                paper_bgcolor: '#0b0e14',
                plot_bgcolor: '#0b0e14'
            }};
            Plotly.newPlot('candlestick-chart', [trace], layout);
        }})
        .catch(e => document.getElementById('candlestick-chart').innerHTML = '<p style="color:#ff1744;">Errore: ' + e + '</p>');
    }}
    loadChart();
    </script>
    """
    return render_page("💱 Trading", content)

# =====================
# MEDIA
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
        <h3>🔥 Trend Attuali</h3>
        <div class="placeholder">Agente Trend Scanner non ancora attivo. Da implementare.</div>
    </div>
    <div class="table-wrap">
        <h3>📝 Script Generati</h3>
        <div class="placeholder">Agente Script Generator non ancora attivo. Da implementare.</div>
    </div>
    <div class="table-wrap">
        <h3>🎬 Video Prodotti</h3>
        <div class="placeholder">Agente Video Creator non ancora attivo. Da implementare.</div>
    </div>
    <div class="table-wrap">
        <h3>📤 Pubblicazioni</h3>
        <div class="placeholder">Agente Publisher non ancora attivo. Da implementare.</div>
    </div>
    """
    return render_page("🎬 Media Company", content)

# =====================
# ECOMMERCE
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
# VERIFIER
# =====================
@app.route('/verifier')
def verifier():
    status = {}
    try:
        with open('/home/carlo/AI_Trading/docs/verification/last_status.json') as f:
            status = json.load(f)
    except: pass
    content = f"""
    <div class="kpi-grid">
        <div class="kpi-card"><div class="label">Ultimo File</div><div class="value" style="font-size:16px;">{status.get('file', 'N/A')}</div></div>
        <div class="kpi-card"><div class="label">Esito</div><div class="value" style="color:{'#00c853' if status.get('success') else '#ff1744'};">{'PASS' if status.get('success') else 'FAIL' if status else 'N/A'}</div></div>
        <div class="kpi-card"><div class="label">Timestamp</div><div class="value" style="font-size:14px;">{status.get('timestamp', 'N/A')[:19] if status.get('timestamp') else 'N/A'}</div></div>
    </div>
    <div class="table-wrap">
        <h3>📋 Output Ultimo Test</h3>
        <pre style="background:#0b0e14;padding:12px;border-radius:8px;color:#78828c;font-size:12px;white-space:pre-wrap;">{status.get('output_tail', 'Nessun output')}</pre>
    </div>
    """
    return render_page("✅ Verifier", content)

# =====================
# API
# =====================
@app.route('/api/chart_data', methods=['POST'])
def chart_data():
    data = request.json
    symbol = data.get('symbol', 'EURUSD=X')
    period = data.get('period', '30d')
    interval = data.get('interval', '1d')
    try:
        df = yf.download(symbol, period=period, interval=interval, multi_level_index=False)
        if df.empty:
            return jsonify({'error': 'Nessun dato'})
        df = df[['Open','High','Low','Close']].tail(100).reset_index()
        records = df.to_dict(orient='records')
        for r in records:
            if 'Date' in r:
                r['Date'] = r['Date'].strftime('%Y-%m-%d %H:%M')
        return jsonify(records)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/verification_status')
def verification_status():
    status_file = '/home/carlo/AI_Trading/docs/verification/last_status.json'
    if os.path.exists(status_file):
        with open(status_file) as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/api/command', methods=['POST'])
def command():
    cmd = request.json.get('cmd')
    if cmd == 'start':
        os.system("cd /home/carlo/AI_Trading && tmux new-session -d -s ai_workforce 'bash -c \"source ~/AI_Trading_Agents/venv/bin/activate && while true; do python3 orchestrator.py; sleep 3600; done\"'")
        return jsonify({'message': '▶️ Avviato'})
    elif cmd == 'stop':
        os.system("tmux kill-session -t ai_workforce 2>/dev/null")
        return jsonify({'message': '⛔ Fermato'})
    elif cmd == 'restart':
        os.system("tmux kill-session -t ai_workforce 2>/dev/null; cd /home/carlo/AI_Trading && tmux new-session -d -s ai_workforce 'bash -c \"source ~/AI_Trading_Agents/venv/bin/activate && while true; do python3 orchestrator.py; sleep 3600; done\"'")
        return jsonify({'message': '🔄 Riavviato'})
    return jsonify({'message': 'Comando sconosciuto'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
