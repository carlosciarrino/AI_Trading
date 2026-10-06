from flask import Flask, render_template_string, jsonify, request, send_from_directory
import json, os, subprocess, yfinance as yf
from datetime import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI_BRIDGE V3 · Control Panel</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #0b0e14; color: #e5e9f0; display: flex; min-height: 100vh; }
        .sidebar { width: 240px; background: #131722; border-right: 1px solid #2a2e39; padding: 24px 16px; display: flex; flex-direction: column; flex-shrink: 0; height: 100vh; position: sticky; top: 0; }
        .sidebar .logo { font-size: 20px; font-weight: 700; margin-bottom: 32px; display: flex; align-items: center; gap: 10px; }
        .sidebar .logo span { background: linear-gradient(135deg, #2962ff, #7c3aed); padding: 6px 10px; border-radius: 8px; font-size: 14px; }
        .sidebar nav a { color: #78828c; text-decoration: none; padding: 10px 14px; border-radius: 8px; font-size: 14px; font-weight: 500; display: block; cursor: pointer; }
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
        .order-panel { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 20px 24px; display: flex; flex-wrap: wrap; align-items: flex-end; gap: 16px; }
        .order-panel label { font-size: 13px; color: #78828c; display: flex; flex-direction: column; gap: 4px; }
        .order-panel select, .order-panel input { background: #1e222d; border: 1px solid #2a2e39; border-radius: 8px; padding: 8px 14px; color: #e5e9f0; font-size: 14px; width: 120px; }
        .order-panel .btn-buy { background: #00c853; color: #0b0e14; border: none; border-radius: 40px; padding: 10px 24px; font-weight: 600; cursor: pointer; }
        .order-panel .btn-sell { background: #ff1744; color: #fff; border: none; border-radius: 40px; padding: 10px 24px; font-weight: 600; cursor: pointer; }
        .table-wrap { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 16px 20px; margin-bottom: 28px; overflow-x: auto; }
        .table-wrap h3 { font-size: 16px; font-weight: 600; margin-bottom: 12px; }
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        th { text-align: left; padding: 10px 8px; color: #78828c; border-bottom: 1px solid #2a2e39; }
        td { padding: 10px 8px; border-bottom: 1px solid #1e222d; }
        .buy { color: #00c853; font-weight: 600; }
        .sell { color: #ff1744; font-weight: 600; }
        .pnl-positive { color: #00c853; font-weight: 600; }
        .pnl-negative { color: #ff1744; font-weight: 600; }
        .log-box { background: #0b0e14; border: 1px solid #2a2e39; border-radius: 12px; padding: 16px 20px; max-height: 200px; overflow-y: auto; font-family: monospace; font-size: 12px; color: #78828c; white-space: pre-wrap; }
        @media (max-width: 768px) { .sidebar { display: none; } .main { padding: 16px; } .kpi-grid { grid-template-columns: 1fr 1fr; } .order-panel { flex-direction: column; align-items: stretch; } .order-panel input { width: 100%; } }
    </style>
    <script src="https://cdn.plot.ly/plotly-2.27.1.min.js"></script>
</head>
<body>
<div class="sidebar">
    <div class="logo"><span>▲</span> AI_BRIDGE</div>
    <nav>
        <a class="active" onclick="showSection('dashboard')">📊 Dashboard</a>
        <a onclick="showSection('trading')">📈 Trading</a>
        <a onclick="showSection('config')">⚙️ Configura</a>
        <a onclick="showSection('log')">📜 Log</a>
    </nav>
    <div class="footer">v3.0 · {{ now }}</div>
</div>
<div class="main">
    <div class="header">
        <h1 id="section-title">📊 Dashboard</h1>
        <div class="status"><span class="dot online" id="status_dot"></span><span id="status_text">Online</span><span style="color:#4a5568;">|</span><span id="last_update">{{ now }}</span></div>
    </div>

    <!-- Banner Verifica -->
    <div id="verification-banner">
        <strong>Stato Verifica:</strong> <span id="verification-text">Nessuna verifica recente</span>
    </div>

    <!-- Sezione Dashboard -->
    <div id="section-dashboard" class="section active">
        <div class="kpi-grid">
            <div class="kpi-card"><div class="label">Capitale</div><div class="value" id="kpi_capital">100.000,00</div></div>
            <div class="kpi-card"><div class="label">PNL Giorno</div><div class="value" id="kpi_pnl">+0,00</div></div>
            <div class="kpi-card"><div class="label">Operazioni Aperte</div><div class="value" id="kpi_open">0</div></div>
            <div class="kpi-card"><div class="label">Drawdown Max</div><div class="value" id="kpi_dd">0,00%</div></div>
        </div>
        <div class="controls">
            <button class="start" onclick="sendCommand('start')">▶ Avvia</button>
            <button class="stop" onclick="sendCommand('stop')">⏹ Ferma</button>
            <button class="restart" onclick="sendCommand('restart')">🔄 Riavvia</button>
        </div>
        <div class="table-wrap"><h3>📋 Operazioni Aperte</h3><table><tr><th>Stato</th><th>Azione</th><th>Lotti</th><th>Prezzo</th><th>SL</th><th>TP</th><th>Orario</th><th>PNL</th></tr>{% for o in orders if o.status == "open" %}<tr><td>{{ o.status }}</td><td class="{{ o.action }}">{{ o.action }}</td><td>{{ o.lots }}</td><td>{{ o.price }}</td><td>{{ o.sl }}</td><td>{{ o.tp }}</td><td>{{ o.time|int|timestamp }}</td><td>{{ o.pnl|default(0) }}</td></tr>{% else %}<tr><td colspan="8" style="text-align:center;color:#4a5568;">Nessuna operazione aperta</td></tr>{% endfor %}</table></div>
        <div class="table-wrap"><h3>📊 Operazioni Chiuse</h3><table><tr><th>Azione</th><th>Lotti</th><th>Prezzo</th><th>Chiusura</th><th>PNL</th><th>Orario</th></tr>{% for o in orders if o.status == "closed" %}<tr><td class="{{ o.action }}">{{ o.action }}</td><td>{{ o.lots }}</td><td>{{ o.price }}</td><td>{{ o.close_price }}</td><td class="pnl-{{ 'positive' if o.pnl > 0 else 'negative' }}">{{ o.pnl }}</td><td>{{ o.time|int|timestamp }}</td></tr>{% else %}<tr><td colspan="6" style="text-align:center;color:#4a5568;">Nessuna operazione chiusa</td></tr>{% endfor %}</table></div>
    </div>

    <!-- Sezione Trading -->
    <div id="section-trading" class="section">
        <div class="chart-container">
            <h3>📈 Grafico {{ selected_symbol }}</h3>
            <div id="candlestick-chart" style="height:400px;"></div>
            <div style="display:flex; gap:16px; margin-top:12px; flex-wrap:wrap;">
                <label>Simbolo
                    <select id="chart_symbol" onchange="loadChart()">
                        <option value="EURUSD=X" selected>EUR/USD</option>
                        <option value="GBPUSD=X">GBP/USD</option>
                        <option value="GC=F">XAU/USD (Oro)</option>
                        <option value="^IXIC">NAS100</option>
                    </select>
                </label>
                <label>Timeframe
                    <select id="chart_interval" onchange="loadChart()">
                        <option value="1m">1 min</option>
                        <option value="5m">5 min</option>
                        <option value="15m" selected>15 min</option>
                        <option value="30m">30 min</option>
                        <option value="1h">1 ora</option>
                        <option value="4h">4 ore</option>
                        <option value="1d">Daily</option>
                    </select>
                </label>
                <label>Periodo
                    <select id="chart_period" onchange="loadChart()">
                        <option value="30d">1 mese</option>
                        <option value="90d">3 mesi</option>
                        <option value="180d">6 mesi</option>
                        <option value="1y">1 anno</option>
                    </select>
                </label>
                <button onclick="loadChart()" style="background:#2962ff;border:none;border-radius:40px;padding:10px 24px;color:#fff;font-weight:600;cursor:pointer;">Aggiorna</button>
            </div>
        </div>
        <div class="order-panel">
            <h3 style="width:100%;">📝 Piazzare ordine manuale</h3>
            <label>Azione
                <select id="order_action">
                    <option value="buy">BUY</option>
                    <option value="sell">SELL</option>
                </select>
            </label>
            <label>Lotti
                <input type="number" id="order_lots" value="0.01" step="0.01" min="0.01">
            </label>
            <label>Prezzo
                <input type="number" id="order_price" step="0.00001" value="1.0">
            </label>
            <label>SL
                <input type="number" id="order_sl" step="0.00001" value="0.999">
            </label>
            <label>TP
                <input type="number" id="order_tp" step="0.00001" value="1.001">
            </label>
            <button class="btn-buy" onclick="placeOrder('buy')">▶ Piazza BUY</button>
            <button class="btn-sell" onclick="placeOrder('sell')">▶ Piazza SELL</button>
            <span id="order_result" style="color:#78828c;font-size:13px;"></span>
        </div>
    </div>

    <!-- Sezione Configura -->
    <div id="section-config" class="section">
        <div class="config-area">
            <label>Timeframe
                <select id="tf_select">
                    <option value="5min">5 min</option>
                    <option value="15min" selected>15 min</option>
                    <option value="1h">1 ora</option>
                    <option value="4h">4 ore</option>
                </select>
            </label>
            <label>Lotto
                <input type="number" id="lot_input" step="0.01" value="0.01">
            </label>
            <button class="save-btn" onclick="saveConfig()">💾 Salva</button>
            <span id="config_msg" style="color:#78828c;font-size:13px;"></span>
        </div>
    </div>

    <!-- Sezione Log -->
    <div id="section-log" class="section">
        <div class="log-box" id="log_box">{{ log }}</div>
        <button onclick="refreshLog()" style="margin-top:12px; background:#2a2e39; border:none; border-radius:40px; padding:8px 24px; color:#e5e9f0; cursor:pointer;">🔄 Aggiorna Log</button>
    </div>
</div>

<script>
    function showSection(id) {
        document.querySelectorAll('.section').forEach(el => el.classList.remove('active'));
        document.getElementById('section-' + id).classList.add('active');
        document.querySelectorAll('.sidebar nav a').forEach(el => el.classList.remove('active'));
        document.querySelector('.sidebar nav a[onclick*="' + id + '"]').classList.add('active');
        document.getElementById('section-title').innerText = document.querySelector('.sidebar nav a[onclick*="' + id + '"]').innerText;
        if (id === 'trading') { loadChart(); }
        if (id === 'log') { refreshLog(); }
    }

    function loadChart() {
        const symbol = document.getElementById('chart_symbol').value;
        const interval = document.getElementById('chart_interval').value;
        const period = document.getElementById('chart_period').value;
        fetch('/chart_data', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({symbol: symbol, period: period, interval: interval})
        })
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                document.getElementById('candlestick-chart').innerHTML = '<p style="color:#ff1744;">' + data.error + '</p>';
                return;
            }
            const trace = {
                x: data.map(d => d.Date),
                open: data.map(d => d.Open),
                high: data.map(d => d.High),
                low: data.map(d => d.Low),
                close: data.map(d => d.Close),
                type: 'candlestick',
                increasing: {line: {color: '#00c853'}},
                decreasing: {line: {color: '#ff1744'}}
            };
            const layout = {
                template: 'plotly_dark',
                xaxis: {title: 'Data', type: 'date'},
                yaxis: {title: 'Prezzo'},
                margin: {l: 40, r: 20, t: 20, b: 40},
                paper_bgcolor: '#0b0e14',
                plot_bgcolor: '#0b0e14'
            };
            Plotly.newPlot('candlestick-chart', [trace], layout);
        })
        .catch(e => {
            document.getElementById('candlestick-chart').innerHTML = '<p style="color:#ff1744;">Errore: ' + e + '</p>';
        });
    }

    function placeOrder(action) {
        const lots = parseFloat(document.getElementById('order_lots').value);
        const price = parseFloat(document.getElementById('order_price').value);
        const sl = parseFloat(document.getElementById('order_sl').value);
        const tp = parseFloat(document.getElementById('order_tp').value);
        if (!lots || !price) { alert('Inserisci lotti e prezzo'); return; }
        document.getElementById('order_result').innerText = '⏳ Invio ordine...';
        fetch('/place_order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: action, lots: lots, price: price, sl: sl, tp: tp})
        })
        .then(r => r.json())
        .then(data => {
            document.getElementById('order_result').innerText = data.message;
        })
        .catch(e => document.getElementById('order_result').innerText = '❌ Errore: ' + e);
    }

    function saveConfig() {
        const data = {
            timeframe: document.getElementById('tf_select').value,
            lot: parseFloat(document.getElementById('lot_input').value)
        };
        fetch('/config', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(r => r.json())
        .then(d => document.getElementById('config_msg').innerText = '✅ ' + d.message)
        .catch(e => document.getElementById('config_msg').innerText = '❌ Errore');
    }

    function sendCommand(cmd) {
        fetch('/command', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({cmd: cmd})
        })
        .then(r => r.json())
        .then(d => alert(d.message))
        .catch(e => alert('Errore: ' + e));
    }

    function refreshLog() {
        fetch('/log')
            .then(r => r.text())
            .then(text => document.getElementById('log_box').innerText = text)
            .catch(e => console.error(e));
    }

    function loadOrders() {
        fetch('/orders')
            .then(r => r.json())
            .then(data => {
                document.getElementById('kpi_open').innerText = data.open || 0;
            })
            .catch(e => console.error(e));
    }

    function loadVerificationStatus() {
        fetch('/verification_status')
            .then(r => r.json())
            .then(data => {
                const banner = document.getElementById('verification-banner');
                const text = document.getElementById('verification-text');
                if (!data || !data.timestamp) {
                    banner.style.display = 'none';
                    return;
                }
                banner.style.display = 'block';
                const date = new Date(data.timestamp).toLocaleString('it-IT');
                if (data.success) {
                    banner.style.background = '#0d3d1e';
                    banner.style.color = '#00c853';
                    text.innerText = `✅ ${data.file} - PASS (${date})`;
                } else {
                    banner.style.background = '#3d0d0d';
                    banner.style.color = '#ff1744';
                    text.innerText = `❌ ${data.file} - FAIL (${date}): ${(data.output_tail || '').substring(0, 200)}`;
                }
            })
            .catch(e => console.error(e));
    }

    setInterval(() => {
        fetch('/status')
            .then(r => r.json())
            .then(data => {
                const dot = document.getElementById('status_dot');
                const txt = document.getElementById('status_text');
                if (data.status === 'online') { dot.className = 'dot online'; txt.innerText = 'Online'; }
                else { dot.className = 'dot offline'; txt.innerText = 'Offline'; }
            });
        loadOrders();
        loadVerificationStatus();
    }, 5000);

    fetch('/config').then(r => r.json()).then(cfg => {
        if (cfg.timeframe) document.getElementById('tf_select').value = cfg.timeframe;
        if (cfg.lot) document.getElementById('lot_input').value = cfg.lot;
    });

    loadVerificationStatus();
</script>
</body>
</html>
"""

@app.template_filter('timestamp')
def timestamp_filter(s):
    try:
        return datetime.fromtimestamp(int(s)).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(s)

@app.route('/')
def index():
    orders = []
    try:
        with open(os.path.expanduser('~/mt4_shared/orders.json')) as f:
            orders = json.load(f)
    except:
        pass
    log = ""
    try:
        with open('/home/carlo/orchestrator.log') as f:
            log = f.read()[-2000:]
    except:
        pass
    return render_template_string(HTML, orders=orders, log=log, now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/chart_data', methods=['POST'])
def chart_data():
    data = request.json
    symbol = data.get('symbol', 'EURUSD=X')
    period = data.get('period', '30d')
    interval = data.get('interval', '1d')
    try:
        df = yf.download(symbol, period=period, interval=interval, multi_level_index=False)
        if df.empty:
            return jsonify({'error': 'Nessun dato'})
        df = df[['Open','High','Low','Close']].tail(100)
        df = df.reset_index()
        records = df.to_dict(orient='records')
        for r in records:
            if 'Date' in r:
                r['Date'] = r['Date'].strftime('%Y-%m-%d %H:%M')
        return jsonify(records)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.json
    action = data.get('action')
    lots = data.get('lots')
    price = data.get('price')
    sl = data.get('sl')
    tp = data.get('tp')
    try:
        from core.mt4_bridge import MT4Bridge
        bridge = MT4Bridge()
        bridge.connect()
        bridge.place_order(action, lots, price, sl, tp)
        bridge.disconnect()
        return jsonify({'status': 'ok', 'message': f'Ordine {action} {lots} @ {price} inviato'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/orders')
def orders_api():
    try:
        with open(os.path.expanduser('~/mt4_shared/orders.json')) as f:
            orders = json.load(f)
        open_orders = [o for o in orders if o.get('status') == 'open']
        return jsonify({'open': len(open_orders)})
    except:
        return jsonify({'open': 0})

@app.route('/log')
def log_api():
    try:
        with open('/home/carlo/orchestrator.log') as f:
            return f.read()[-2000:]
    except:
        return ""

@app.route('/verification_status')
def verification_status():
    status_file = '/home/carlo/AI_Trading/docs/verification/last_status.json'
    if os.path.exists(status_file):
        try:
            with open(status_file) as f:
                return jsonify(json.load(f))
        except:
            pass
    return jsonify({})

@app.route('/command', methods=['POST'])
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

@app.route('/config', methods=['GET', 'POST'])
def config():
    config_path = '/home/carlo/AI_Trading/config.json'
    if request.method == 'GET':
        try:
            with open(config_path) as f:
                return jsonify(json.load(f))
        except:
            return jsonify({'timeframe': '15min', 'lot': 0.01})
    data = request.json
    try:
        with open(config_path) as f:
            cfg = json.load(f)
    except:
        cfg = {}
    cfg.update(data)
    with open(config_path, 'w') as f:
        json.dump(cfg, f, indent=2)
    return jsonify({'message': f'Config salvata: {cfg}'})

@app.route('/status')
def status():
    online = os.system("tmux list-sessions | grep -q ai_workforce") == 0
    return jsonify({'status': 'online' if online else 'offline'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
