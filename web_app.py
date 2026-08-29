from flask import Flask, render_template_string, jsonify, request
import json, os, subprocess
from datetime import datetime

app = Flask(__name__)

AGENTS = {
    "ai_workforce": {"name": "Orchestratore", "task": "Prende decisioni di trading tramite AI e gestisce il flusso dati."},
    "dashboard": {"name": "Dashboard", "task": "Mostra lo stato dell'azienda all'utente."},
    "sentinel": {"name": "Sentinella", "task": "Monitora la sicurezza e ferma il sistema in caso di anomalie."},
    "news_agent": {"name": "Agente Notizie", "task": "Analizza notizie macro (guerre, crisi, tassi)."},
    "social_agent": {"name": "Agente Social", "task": "Analizza sentiment da social e news trending."},
    "cycle_agent": {"name": "Agente Cicli", "task": "Analizza cicli storici e stagionalità del mercato."},
    "experience_agent": {"name": "Agente Esperienza", "task": "Impara dagli errori passati e aggiorna la memoria."},
    "strategy_tester_agent": {"name": "Strategy Tester", "task": "Analizza link e testa strategie su dati storici."},
    "github_researcher": {"name": "GitHub Researcher", "task": "Cerca progetti utili su GitHub."},
    "skill_researcher": {"name": "Skill Researcher", "task": "Cerca nuove competenze, framework o strategie online."},
    "news_critical": {"name": "News Critical", "task": "Analizza condizioni socio-politiche globali."},
    "ai_researcher_agent": {"name": "AI Researcher", "task": "Cerca nuove intelligenze artificiali disponibili."},
    "ai_tester_agent": {"name": "AI Tester", "task": "Testa le nuove AI su compiti reali."},
    "sync_agent": {"name": "Sync Agent", "task": "Sincronizza il progetto su GitHub e USB."}
}

AGENT_COMMANDS = {
    "ai_workforce": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 orchestrator.py > /home/carlo/orchestrator.log 2>&1",
    "dashboard": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 web_app.py",
    "sentinel": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 sentinel.py",
    "news_agent": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 news_agent.py",
    "social_agent": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 social_agent.py",
    "cycle_agent": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 cycle_agent.py",
    "experience_agent": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 experience_agent.py",
    "strategy_tester_agent": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 strategy_tester_agent.py",
    "github_researcher": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 github_researcher.py",
    "skill_researcher": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 skill_researcher.py",
    "news_critical": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 news_critical.py",
    "ai_researcher_agent": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 ai_researcher_agent.py",
    "ai_tester_agent": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 ai_tester_agent.py",
    "sync_agent": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 sync_agent.py"
}

def get_status():
    out = subprocess.run(["tmux", "ls"], capture_output=True, text=True)
    sessions = out.stdout if out.returncode == 0 else ""
    status = {}
    for name, info in AGENTS.items():
        status[name] = "active" if name in sessions else "stopped"
    return status

HTML = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI_BRIDGE V5 · Control Panel</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Inter', sans-serif; background: #0b0e14; color: #e5e9f0; display: flex; height: 100vh; }
        .sidebar { width: 220px; background: #131722; border-right: 1px solid #2a2e39; padding: 20px; display: flex; flex-direction: column; flex-shrink: 0; }
        .logo { font-size: 20px; font-weight: 700; margin-bottom: 30px; display: flex; align-items: center; gap: 10px; }
        .logo span { background: #2962ff; padding: 4px 8px; border-radius: 6px; font-size: 14px; }
        .nav { display: flex; flex-direction: column; gap: 5px; }
        .nav a { color: #78828c; text-decoration: none; padding: 10px 12px; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; }
        .nav a:hover, .nav a.active { background: #2a2e39; color: #fff; }
        .footer { margin-top: auto; font-size: 12px; color: #4a5568; border-top: 1px solid #2a2e39; padding-top: 15px; }
        .main { flex: 1; padding: 24px 32px; overflow-y: auto; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .header .status-box { display: flex; align-items: center; gap: 10px; background: #1e222d; padding: 8px 16px; border-radius: 20px; font-size: 14px; }
        .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
        .dot.green { background: #00c853; }
        .dot.red { background: #ff1744; }
        .btn-emergency { background: #ff1744; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .section { display: none; }
        .section.active { display: block; }
        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 30px; }
        .kpi-card { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 20px; }
        .kpi-card .label { font-size: 13px; color: #78828c; }
        .kpi-card .value { font-size: 26px; font-weight: 700; margin-top: 5px; }
        table { width: 100%; border-collapse: collapse; font-size: 14px; }
        th { text-align: left; padding: 12px; color: #78828c; border-bottom: 1px solid #2a2e39; }
        td { padding: 12px; border-bottom: 1px solid #1e222d; }
        .buy { color: #00c853; font-weight: 600; }
        .sell { color: #ff1744; font-weight: 600; }
        .pnl-pos { color: #00c853; font-weight: 600; }
        .pnl-neg { color: #ff1744; font-weight: 600; }
        .table-box { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
        .chart-container { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 16px; margin-bottom: 20px; }
        .chart-container iframe { width: 100%; height: 500px; border: none; border-radius: 8px; }
        .control-row { display: flex; gap: 12px; align-items: flex-end; margin-top: 12px; flex-wrap: wrap; }
        .control-row label { font-size: 13px; color: #78828c; display: flex; flex-direction: column; gap: 4px; }
        .control-row select, .control-row input { background: #1e222d; border: 1px solid #2a2e39; border-radius: 6px; padding: 8px 12px; color: #fff; }
        .btn { background: #2962ff; border: none; border-radius: 6px; padding: 10px 20px; color: #fff; font-weight: 600; cursor: pointer; }
        .btn-buy { background: #00c853; border: none; border-radius: 6px; padding: 10px 20px; color: #000; font-weight: 600; cursor: pointer; }
        .btn-sell { background: #ff1744; border: none; border-radius: 6px; padding: 10px 20px; color: #fff; font-weight: 600; cursor: pointer; }
        .agent-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }
        .agent-card { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 20px; display: flex; flex-direction: column; }
        .agent-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .agent-header h3 { font-size: 16px; }
        .agent-task { font-size: 13px; color: #78828c; margin-bottom: 15px; flex-grow: 1; }
        .agent-status { font-size: 13px; display: flex; align-items: center; gap: 5px; }
        .agent-actions { display: flex; gap: 8px; }
        .btn-start { background: #2962ff; border: none; border-radius: 6px; padding: 6px 12px; color: #fff; font-size: 12px; cursor: pointer; }
        .btn-stop { background: #ff1744; border: none; border-radius: 6px; padding: 6px 12px; color: #fff; font-size: 12px; cursor: pointer; }
        .config-box { background: #131722; border: 1px solid #2a2e39; border-radius: 12px; padding: 24px; margin-bottom: 20px; }
        .config-box h3 { margin-bottom: 20px; border-bottom: 1px solid #2a2e39; padding-bottom: 10px; }
        .config-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .config-grid label { font-size: 13px; color: #78828c; display: block; margin-bottom: 6px; }
        .config-grid input, .config-grid select { width: 100%; background: #1e222d; border: 1px solid #2a2e39; border-radius: 6px; padding: 10px; color: #fff; }
        .log-box { background: #000; padding: 16px; max-height: 300px; overflow-y: auto; font-family: monospace; font-size: 12px; color: #00c853; border-radius: 8px; }
        .btn-orange { background: #ff9800; border: none; border-radius: 6px; padding: 10px 20px; color: #000; font-weight: 600; cursor: pointer; }
        .btn-green { background: #4caf50; border: none; border-radius: 6px; padding: 10px 20px; color: #fff; font-weight: 600; cursor: pointer; }
        .video-status { background: #1e222d; padding: 12px; border-radius: 8px; margin-top: 10px; font-size: 13px; }
        .video-status .ok { color: #4caf50; }
        .video-status .ko { color: #ff1744; }
    </style>
</head>
<body>
<div class="sidebar">
    <div class="logo"><span>▲</span> AI_BRIDGE</div>
    <nav class="nav">
        <a class="active" onclick="switchSection('dashboard')">📊 Dashboard</a>
        <a onclick="switchSection('trading')">📈 Trading</a>
        <a onclick="switchSection('agents')">🤖 Agenti</a>
        <a onclick="switchSection('config')">⚙️ Configura</a>
    </nav>
    <div class="footer">v5.0 · {{ now }}</div>
</div>

<div class="main">
    <div id="dashboard" class="section active">
        <div class="header">
            <h1>📊 Dashboard</h1>
            <div style="display:flex; gap:10px;">
                <div class="status-box"><span class="dot green" id="status_dot"></span><span id="status_text">Caricamento...</span></div>
                <button class="btn-emergency" onclick="emergencyStop()">🛑 STOP TUTTO</button>
            </div>
        </div>
        <div class="kpi-grid">
            <div class="kpi-card"><div class="label">Capitale</div><div class="value">10.000,00</div></div>
            <div class="kpi-card"><div class="label">Operazioni Aperte</div><div class="value" id="kpi_open">0</div></div>
            <div class="kpi-card"><div class="label">PNL Giorno</div><div class="value">+0,00</div></div>
        </div>
        <div class="table-box">
            <h3 style="margin-bottom:15px;">📋 Operazioni Aperte</h3>
            <table>
                <tr><th>Azione</th><th>Lotti</th><th>Prezzo</th><th>SL</th><th>TP</th><th>Orario</th><th>PNL</th></tr>
                {% for o in orders if o.status == "open" %}
                <tr><td class="{{ o.action }}">{{ o.action }}</td><td>{{ o.lots }}</td><td>{{ o.price }}</td><td>{{ o.sl }}</td><td>{{ o.tp }}</td><td>{{ o.time|int|timestamp }}</td><td>{{ o.pnl|default(0) }}</td></tr>
                {% else %}
                <tr><td colspan="7" style="text-align:center; color:#4a5568;">Nessuna operazione aperta</td></tr>
                {% endfor %}
            </table>
        </div>
        <div class="table-box">
            <h3 style="margin-bottom:15px;">📊 Operazioni Chiuse</h3>
            <table>
                <tr><th>Azione</th><th>Lotti</th><th>Prezzo</th><th>Chiusura</th><th>PNL</th><th>Orario</th></tr>
                {% for o in orders if o.status == "closed" %}
                <tr><td class="{{ o.action }}">{{ o.action }}</td><td>{{ o.lots }}</td><td>{{ o.price }}</td><td>{{ o.close_price }}</td><td class="{{ 'pnl-pos' if o.pnl > 0 else 'pnl-neg' }}">{{ o.pnl }}</td><td>{{ o.time|int|timestamp }}</td></tr>
                {% else %}
                <tr><td colspan="6" style="text-align:center; color:#4a5568;">Nessuna operazione chiusa</td></tr>
                {% endfor %}
            </table>
        </div>
    </div>

    <div id="trading" class="section">
        <div class="header"><h1>📈 Trading</h1></div>
        <div class="chart-container">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=FX_IDC%3AEURUSD&interval=D&theme=dark&style=1&locale=it&hidesidetoolbar=1" frameborder="0" allowtransparency="true"></iframe>
        </div>
        <div class="control-row">
            <label>Simbolo
                <select id="symbol_select" onchange="updateChart()">
                    <option value="EURUSD=X" selected>EUR/USD</option>
                    <option value="GBPUSD=X">GBP/USD</option>
                    <option value="GC=F">Oro</option>
                </select>
            </label>
            <label>Timeframe
                <select id="interval_select" onchange="updateChart()">
                    <option value="1m">1 min</option>
                    <option value="5m">5 min</option>
                    <option value="15m">15 min</option>
                    <option value="1h">1 ora</option>
                    <option value="4h">4 ore</option>
                    <option value="1d" selected>Daily</option>
                </select>
            </label>
            <label>Periodo
                <select id="period_select" onchange="updateChart()">
                    <option value="30d">1 mese</option>
                    <option value="90d">3 mesi</option>
                    <option value="1y">1 anno</option>
                </select>
            </label>
            <button class="btn" onclick="updateChart()">Aggiorna</button>
        </div>
        <div class="table-box" style="margin-top:20px;">
            <h3 style="margin-bottom:15px;">Piazzare ordine manuale</h3>
            <div class="control-row">
                <label>Azione
                    <select id="order_action"><option value="buy">BUY</option><option value="sell">SELL</option></select>
                </label>
                <label>Lotti <input type="number" id="order_lots" value="0.01" step="0.01"></label>
                <label>SL <input type="number" id="order_sl" step="0.00001" value="1.0"></label>
                <label>TP <input type="number" id="order_tp" step="0.00001" value="1.0"></label>
                <button class="btn-buy" onclick="placeOrder('buy')">Piazza BUY</button>
                <button class="btn-sell" onclick="placeOrder('sell')">Piazza SELL</button>
            </div>
        </div>
    </div>

    <div id="agents" class="section">
        <div class="header"><h1>🤖 Agenti Aziendali</h1></div>
        <div class="agent-grid" id="agent_grid">
            {% for id, info in agents.items() %}
            <div class="agent-card">
                <div class="agent-header"><h3>{{ info.name }}</h3><span class="agent-status" id="status_{{ id }}"><span class="dot"></span> Caricamento...</span></div>
                <div class="agent-task">{{ info.task }}</div>
                <div class="agent-actions">
                    <button class="btn-start" onclick="controlAgent('{{ id }}', 'start')">Avvia</button>
                    <button class="btn-stop" onclick="controlAgent('{{ id }}', 'stop')">Ferma</button>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <div id="config" class="section">
        <div class="header"><h1>⚙️ Configurazione</h1></div>
        <div class="config-box">
            <h3>Parametri di trading</h3>
            <div class="config-grid">
                <div><label>Timeframe</label><select id="tf_select"><option value="5min">5 min</option><option value="15min" selected>15 min</option><option value="1h">1 ora</option></select></div>
                <div><label>Lotto</label><input type="number" id="lot_input" value="0.01" step="0.01"></div>
                <div><label>Orario di Trading</label><select id="session_select">
                    <option value="all">Tutte le sessioni</option>
                    <option value="london">Londra</option>
                    <option value="newyork">New York</option>
                    <option value="tokyo">Tokyo</option>
                    <option value="london_newyork">Londra + New York</option>
                </select></div>
            </div>
            <button class="btn" style="margin-top:20px;" onclick="saveConfig()">💾 Salva Config</button>
        </div>

        <div class="config-box">
            <h3>🎥 Analizza video (YouTube/Instagram/Facebook/TikTok)</h3>
            <p style="font-size:13px; color:#78828c; margin-bottom:15px;">Incolla il link e premi "Analizza Ora". L'agente scaricherà e trascriverà il video, poi lo analizzerà con AI.</p>
            <div class="control-row">
                <input type="text" id="video_link_input" placeholder="https://..." style="flex:1; background:#1e222d; border:1px solid #2a2e39; border-radius:6px; padding:10px; color:#fff;">
                <button class="btn" onclick="analyzeVideo()">▶️ Analizza Ora</button>
                <button class="btn-green" onclick="leggiReportVideo()">📄 Report</button>
            </div>
            <div id="video_status" class="video-status">Stato: in attesa di analisi</div>
        </div>

        <div class="config-box">
            <h3>📋 Strategy Tester (link generico)</h3>
            <p style="font-size:13px; color:#78828c; margin-bottom:15px;">Incolla un link e l'agente Strategy Tester lo analizzerà.</p>
            <input type="text" id="strategy_link" placeholder="Incolla link qui..." style="width:100%; background:#1e222d; border:1px solid #2a2e39; border-radius:6px; padding:10px; color:#fff; margin-bottom:15px;">
            <button class="btn" onclick="testStrategy()">🚀 Avvia Test</button>
            <button class="btn-green" onclick="leggiReport()">📄 Leggi Report</button>
            <button class="btn-orange" onclick="applicaStrategia()">✅ Applica</button>
        </div>

        <div class="config-box">
            <h3>Log di sistema</h3>
            <div class="log-box" id="log_box">{{ log }}</div>
            <button class="btn" style="margin-top:10px;" onclick="refreshLog()">Aggiorna Log</button>
        </div>
    </div>
</div>

<script>
    function switchSection(sectionId) {
        document.querySelectorAll('.section').forEach(el => el.classList.remove('active'));
        document.getElementById(sectionId).classList.add('active');
        document.querySelectorAll('.nav a').forEach(el => el.classList.remove('active'));
        document.querySelector(`.nav a[onclick*='${sectionId}']`).classList.add('active');
    }

    function fetchStatus() {
        fetch('/status')
        .then(r => r.json())
        .then(data => {
            const dot = document.getElementById('status_dot');
            const txt = document.getElementById('status_text');
            if (data.system_online) {
                dot.className = 'dot green';
                txt.innerText = 'Sistema Online';
            } else {
                dot.className = 'dot red';
                txt.innerText = 'Sistema Offline';
            }
            document.getElementById('kpi_open').innerText = data.open_count || 0;
            for (const [id, status] of Object.entries(data.agents)) {
                const span = document.getElementById('status_' + id);
                if (span) {
                    if (status === 'active') {
                        span.innerHTML = '<span class="dot green"></span> Attivo';
                    } else {
                        span.innerHTML = '<span class="dot red"></span> Fermo';
                    }
                }
            }
        });
    }

    function emergencyStop() {
        if (confirm('SEI SICURO DI VOLER FERMARE TUTTO? Questa azione chiude tutte le operazioni e spegne il sistema.')) {
            fetch('/emergency', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({}) })
            .then(r => r.json())
            .then(d => { alert(d.message); location.reload(); });
        }
    }

    function controlAgent(id, action) {
        fetch('/control', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name: id, action: action})
        })
        .then(r => r.json())
        .then(d => { alert(d.message); fetchStatus(); });
    }

    function updateChart() {
        alert('Aggiornamento grafico in modalità demo.');
    }

    function placeOrder(action) {
        const lots = parseFloat(document.getElementById('order_lots').value);
        const sl = parseFloat(document.getElementById('order_sl').value);
        const tp = parseFloat(document.getElementById('order_tp').value);
        fetch('/place_order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: action, lots: lots, price: 0, sl: sl, tp: tp})
        })
        .then(r => r.json())
        .then(d => alert(d.message));
    }

    function saveConfig() {
        const session = document.getElementById('session_select').value;
        fetch('/config', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({timeframe: document.getElementById('tf_select').value, lot: parseFloat(document.getElementById('lot_input').value), session: session})
        })
        .then(r => r.json())
        .then(d => alert(d.message));
    }

    function analyzeVideo() {
        const link = document.getElementById('video_link_input').value;
        if (!link) { alert('Inserisci un link valido'); return; }
        document.getElementById('video_status').innerHTML = 'Stato: 🔄 Analisi in corso...';
        fetch('/analyze_video', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({link: link})
        })
        .then(r => r.json())
        .then(d => {
            alert(d.message);
            aggiornaStatoVideo();
        })
        .catch(err => {
            document.getElementById('video_status').innerHTML = 'Stato: ❌ Errore durante l\'analisi';
        });
    }

    function aggiornaStatoVideo() {
        fetch('/video_status')
        .then(r => r.json())
        .then(data => {
            if (data.report) {
                document.getElementById('video_status').innerHTML = 'Stato: ✅ Ultima analisi completata alle ' + data.timestamp;
            } else {
                document.getElementById('video_status').innerHTML = 'Stato: ⏳ Nessun report disponibile';
            }
        });
    }

    function leggiReportVideo() {
        fetch('/leggi_report_video')
        .then(r => r.text())
        .then(text => { 
            if (text.trim().length === 0) { alert('Nessun report video disponibile.'); return; }
            const newWindow = window.open('', '_blank');
            newWindow.document.write('<pre style="background:#0b0e14; color:#00c853; padding:20px; font-size:14px; white-space:pre-wrap;">' + text + '</pre>');
        });
    }

    function testStrategy() {
        const link = document.getElementById('strategy_link').value;
        if (!link) { alert('Inserisci un link'); return; }
        fetch('/test_strategy', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({link: link})
        })
        .then(r => r.json())
        .then(d => alert(d.message));
    }

    function leggiReport() {
        fetch('/leggi_report')
        .then(r => r.text())
        .then(text => { 
            if (text.trim().length === 0) { alert('Nessun report disponibile.'); return; }
            const newWindow = window.open('', '_blank');
            newWindow.document.write('<pre style="background:#0b0e14; color:#00c853; padding:20px; font-size:14px; white-space:pre-wrap;">' + text + '</pre>');
        });
    }

    function applicaStrategia() {
        fetch('/applica_strategia', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({}) })
        .then(r => r.json())
        .then(d => alert(d.message));
    }

    function refreshLog() {
        fetch('/log')
        .then(r => r.text())
        .then(text => document.getElementById('log_box').innerText = text);
    }

    // Aggiorna stato video all'avvio
    aggiornaStatoVideo();
    setInterval(fetchStatus, 5000);
    fetchStatus();
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
    return render_template_string(HTML, orders=orders, log=log, now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), agents=AGENTS)

@app.route('/status')
def status():
    status = get_status()
    open_count = 0
    try:
        with open(os.path.expanduser('~/mt4_shared/orders.json')) as f:
            orders = json.load(f)
        open_count = len([o for o in orders if o.get('status') == 'open'])
    except:
        pass
    return jsonify({'system_online': any(v == 'active' for v in status.values()), 'agents': status, 'open_count': open_count})

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    name = data.get('name')
    action = data.get('action')
    if action == 'start':
        if name in AGENT_COMMANDS:
            os.system(f"tmux new-session -d -s {name} \"{AGENT_COMMANDS[name]}\"")
            return jsonify({'message': f'{name} avviato'})
    else:
        os.system(f"tmux kill-session -t {name} 2>/dev/null")
        return jsonify({'message': f'{name} fermato'})
    return jsonify({'message': 'Azione non valida'})

@app.route('/emergency', methods=['POST'])
def emergency():
    os.system("tmux kill-server 2>/dev/null")
    return jsonify({'message': '🛑 SISTEMA FERMATO. Tutte le operazioni sono state chiuse.'})

@app.route('/place_order', methods=['POST'])
def place_order():
    return jsonify({'message': 'Ordine manuale inviato (placeholder)'})

@app.route('/config', methods=['GET', 'POST'])
def config():
    config_path = '/home/carlo/AI_Trading/config.json'
    if request.method == 'GET':
        try:
            with open(config_path) as f:
                return jsonify(json.load(f))
        except:
            return jsonify({'timeframe': '15min', 'lot': 0.01, 'session': 'all'})
    data = request.json
    try:
        with open(config_path) as f:
            cfg = json.load(f)
    except:
        cfg = {}
    cfg.update(data)
    with open(config_path, 'w') as f:
        json.dump(cfg, f, indent=2)
    return jsonify({'message': 'Config salvata'})

@app.route('/test_strategy', methods=['POST'])
def test_strategy():
    data = request.json
    link = data.get('link')
    with open('/home/carlo/AI_Trading/strategia_da_testare.txt', 'w') as f:
        f.write(link)
    return jsonify({'message': f'Strategia inviata al tester: {link}'})

@app.route('/leggi_report')
def leggi_report():
    try:
        with open('/home/carlo/AI_Trading/report_strategia.txt', 'r') as f:
            return f.read()
    except:
        return ""

@app.route('/applica_strategia', methods=['POST'])
def applica_strategia():
    with open('/home/carlo/AI_Trading/segnali/backtest_richiesto.txt', 'w') as f:
        f.write("1")
    return jsonify({'message': 'Backtest avviato. L\'agente tester lavorerà di notte.'})

@app.route('/log')
def log_api():
    try:
        with open('/home/carlo/orchestrator.log') as f:
            return f.read()[-2000:]
    except:
        return ""

# ----- NUOVE ROTTE PER VIDEO ANALYZER -----
@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    data = request.json
    link = data.get('link')
    if not link:
        return jsonify({'message': 'Link mancante'}), 400
    # Scrivi link in video_link.txt
    with open('/home/carlo/AI_Trading/video_link.txt', 'w') as f:
        f.write(link)
    # Avvia lo script multidigest.py in background (senza attendere)
    subprocess.Popen(["python3", "/home/carlo/AI_Trading/multidigest.py"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     cwd="/home/carlo/AI_Trading")
    return jsonify({'message': f'Analisi avviata per: {link}'})

@app.route('/video_status')
def video_status():
    report_path = '/home/carlo/AI_Trading/report_multivideo.txt'
    try:
        with open(report_path, 'r') as f:
            content = f.read()
        # Estrai timestamp dalla prima riga
        lines = content.split('\n')
        ts = lines[0].replace('REPORT MULTI-VIDEO - ', '').strip()
        return jsonify({'report': content[:500], 'timestamp': ts})
    except:
        return jsonify({'report': None, 'timestamp': None})

@app.route('/leggi_report_video')
def leggi_report_video():
    try:
        with open('/home/carlo/AI_Trading/report_multivideo.txt', 'r') as f:
            return f.read()
    except:
        return ""
# ----- FINE NUOVE ROTTE -----

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
