from flask import Flask, render_template_string, jsonify, request
import json, os, subprocess, threading, time
from datetime import datetime

app = Flask(__name__)

# ELENCO COMPLETO DEGLI AGENTI (aggiornato con tutti quelli noti)
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
    "sync_agent": {"name": "Sync Agent", "task": "Sincronizza il progetto su GitHub e USB."},
    "supervisor": {"name": "Supervisor", "task": "Riavvia automaticamente gli agenti critici se si fermano."},
    "tool_updater": {"name": "Tool Updater", "task": "Cerca nuovi strumenti di trascrizione e analisi video."},
    "yt_digest": {"name": "YT Digest", "task": "Analizza video notturni con panoscribe."}
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
    "sync_agent": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 sync_agent.py",
    "supervisor": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 supervisor_agent.py",
    "tool_updater": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 tool_updater_agent.py",
    "yt_digest": "cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 yt_digest.py"
}

def get_status():
    out = subprocess.run(["tmux", "ls"], capture_output=True, text=True)
    sessions = out.stdout if out.returncode == 0 else ""
    status = {}
    for name, info in AGENTS.items():
        status[name] = "active" if name in sessions else "stopped"
    return status

# ----- AUDIT BACKGROUND -----
AUDIT_INTERVAL = 300
AUDIT_JSON = os.path.expanduser("~/AI_Trading/audit_status.json")
audit_data = {"has_issue": False, "agents": {}, "critical": {}, "timestamp": ""}

def run_audit_loop():
    global audit_data
    while True:
        try:
            subprocess.run(["python3", "/home/carlo/AI_Trading/audit_agent.py"],
                           capture_output=True, cwd="/home/carlo/AI_Trading")
            if os.path.exists(AUDIT_JSON):
                with open(AUDIT_JSON, "r") as f:
                    audit_data = json.load(f)
        except Exception as e:
            print(f"Audit error: {e}")
        time.sleep(AUDIT_INTERVAL)

threading.Thread(target=run_audit_loop, daemon=True).start()
# ----- FINE AUDIT -----

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI_BRIDGE V5</title>
    <style>
        body { font-family: sans-serif; background: #0b0e14; color: #e5e9f0; margin:0; }
        .sidebar { width: 200px; background: #131722; position: fixed; height:100%; padding:20px; }
        .main { margin-left: 220px; padding:20px; }
        .nav a { display:block; padding:10px; color:#78828c; text-decoration:none; cursor:pointer; }
        .nav a:hover { background:#2a2e39; color:#fff; }
        .section { display:none; }
        .section.active { display:block; }
        .btn { background: #2962ff; border:none; padding:8px 16px; border-radius:4px; color:#fff; cursor:pointer; }
        .btn-emergency { background: #ff1744; }
        .dot { display:inline-block; width:10px; height:10px; border-radius:50%; }
        .dot.green { background: #00c853; }
        .dot.red { background: #ff1744; }
        .status-box { display:inline-block; background:#1e222d; padding:6px 12px; border-radius:20px; }
        table { width:100%; border-collapse:collapse; }
        th, td { padding:8px; border-bottom:1px solid #2a2e39; text-align:left; }
        .buy { color:#00c853; }
        .sell { color:#ff1744; }
        .config-box { background:#131722; padding:20px; margin-bottom:20px; border-radius:8px; border:1px solid #2a2e39; }
        input, select { background:#1e222d; border:1px solid #2a2e39; padding:8px; color:#fff; border-radius:4px; }
        .log-box { background:#000; padding:16px; max-height:300px; overflow-y:auto; font-family:monospace; font-size:12px; color:#00c853; border-radius:8px; }
        .alert-banner { background:#ff1744; color:#fff; padding:12px 20px; text-align:center; font-weight:bold; border-radius:8px; margin-bottom:20px; }
        .audit-box { background:#131722; padding:16px; border-radius:8px; border:1px solid #2a2e39; margin-bottom:20px; }
        .agent-status-badge { display:inline-block; background:#1e222d; padding:6px 12px; border-radius:20px; margin-right:8px; }
    </style>
</head>
<body>
<div class="sidebar">
    <h2>▲ AI_BRIDGE</h2>
    <nav class="nav">
        <a onclick="showSection('dashboard')">📊 Dashboard</a>
        <a onclick="showSection('trading')">📈 Trading</a>
        <a onclick="showSection('agents')">🤖 Agenti</a>
        <a onclick="showSection('config')">⚙️ Configura</a>
    </nav>
    <div style="margin-top:40px; font-size:12px; color:#4a5568;">v5.0 · {{ now }}</div>
</div>

<div class="main">
    {% if audit_data.has_issue %}
    <div class="alert-banner">
        ⚠️ ALLARME: uno o più agenti critici sono FERMI! Controlla la sezione Agenti.
    </div>
    {% endif %}

    <!-- DASHBOARD -->
    <div id="section-dashboard" class="section active">
        <h1>📊 Dashboard</h1>
        <div style="display:flex; gap:20px; flex-wrap:wrap;">
            <button class="btn" onclick="fetchStatus()">🔄 Aggiorna stato</button>
            <div class="status-box"><span class="dot green" id="status_dot"></span> <span id="status_text">Caricamento...</span></div>
            <button class="btn btn-emergency" onclick="emergencyStop()">🛑 STOP TUTTO</button>
        </div>
        <div id="status_log" style="color:#78828c; margin:16px 0;">📡 Ultimo aggiornamento: --</div>

        <!-- Audit box con TUTTI gli agenti -->
        <div class="audit-box">
            <h3>🔍 Stato Agenti (Audit automatico)</h3>
            <div style="font-size:13px; color:#78828c;">
                Ultimo controllo: {{ audit_data.timestamp if audit_data.timestamp else 'Nessun controllo effettuato.' }}
            </div>
            <div style="display:flex; gap:16px; flex-wrap:wrap; margin-top:8px;">
                {% for agent, status in audit_data.agents.items() %}
                <div class="agent-status-badge">
                    <span style="color:{{ '#00c853' if status == 'active' else '#ff1744' }};">●</span>
                    {{ agent }}: {{ status }}
                </div>
                {% endfor %}
            </div>
        </div>

        <div style="display:flex; gap:20px;">
            <div style="background:#131722; padding:20px; border-radius:8px; flex:1;"><div>Capitale</div><div style="font-size:24px;">10.000,00</div></div>
            <div style="background:#131722; padding:20px; border-radius:8px; flex:1;"><div>Operazioni Aperte</div><div style="font-size:24px;" id="kpi_open">0</div></div>
            <div style="background:#131722; padding:20px; border-radius:8px; flex:1;"><div>PNL Giorno</div><div style="font-size:24px;">+0,00</div></div>
        </div>
        <div style="background:#131722; padding:20px; border-radius:8px; margin-top:20px;">
            <h3>📋 Operazioni Aperte</h3>
            <table>
                <tr><th>Azione</th><th>Lotti</th><th>Prezzo</th><th>SL</th><th>TP</th><th>Orario</th><th>PNL</th></tr>
                {% for o in orders if o.status == "open" %}
                <tr><td class="{{ o.action }}">{{ o.action }}</td><td>{{ o.lots }}</td><td>{{ o.price }}</td><td>{{ o.sl }}</td><td>{{ o.tp }}</td><td>{{ o.time|int|timestamp }}</td><td>{{ o.pnl|default(0) }}</td></tr>
                {% else %}
                <tr><td colspan="7" style="color:#4a5568;">Nessuna operazione aperta</td></tr>
                {% endfor %}
            </table>
        </div>
        <div style="background:#131722; padding:20px; border-radius:8px; margin-top:20px;">
            <h3>📊 Operazioni Chiuse</h3>
            <table>
                <tr><th>Azione</th><th>Lotti</th><th>Prezzo</th><th>Chiusura</th><th>PNL</th><th>Orario</th></tr>
                {% for o in orders if o.status == "closed" %}
                <tr><td class="{{ o.action }}">{{ o.action }}</td><td>{{ o.lots }}</td><td>{{ o.price }}</td><td>{{ o.close_price }}</td><td class="{{ 'pnl-pos' if o.pnl > 0 else 'pnl-neg' }}">{{ o.pnl }}</td><td>{{ o.time|int|timestamp }}</td></tr>
                {% else %}
                <tr><td colspan="6" style="color:#4a5568;">Nessuna operazione chiusa</td></tr>
                {% endfor %}
            </table>
        </div>
    </div>

    <!-- TRADING -->
    <div id="section-trading" class="section">
        <h1>📈 Trading</h1>
        <div style="background:#131722; padding:20px; border-radius:8px;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=FX_IDC%3AEURUSD&interval=D&theme=dark&style=1&locale=it&hidesidetoolbar=1" style="width:100%; height:400px; border:none; border-radius:8px;"></iframe>
        </div>
        <div style="background:#131722; padding:20px; border-radius:8px; margin-top:20px;">
            <h3>Piazzare ordine manuale</h3>
            <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:flex-end;">
                <label>Azione<select id="order_action"><option value="buy">BUY</option><option value="sell">SELL</option></select></label>
                <label>Lotti <input type="number" id="order_lots" value="0.01" step="0.01"></label>
                <label>SL <input type="number" id="order_sl" step="0.00001" value="1.0"></label>
                <label>TP <input type="number" id="order_tp" step="0.00001" value="1.0"></label>
                <button class="btn" onclick="placeOrder('buy')">Piazza BUY</button>
                <button class="btn" style="background:#ff1744;" onclick="placeOrder('sell')">Piazza SELL</button>
            </div>
        </div>
    </div>

    <!-- AGENTI -->
    <div id="section-agents" class="section">
        <h1>🤖 Agenti</h1>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px,1fr)); gap:16px;">
            {% for id, info in agents.items() %}
            <div style="background:#131722; padding:16px; border-radius:8px; border:1px solid #2a2e39;">
                <div style="display:flex; justify-content:space-between;">
                    <h3>{{ info.name }}</h3>
                    <span id="status_{{ id }}"><span class="dot"></span> Caricamento...</span>
                </div>
                <div style="color:#78828c; font-size:13px;">{{ info.task }}</div>
                <div style="margin-top:10px;">
                    <button class="btn" onclick="controlAgent('{{ id }}','start')">Avvia</button>
                    <button class="btn" style="background:#ff1744;" onclick="controlAgent('{{ id }}','stop')">Ferma</button>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- CONFIG -->
    <div id="section-config" class="section">
        <h1>⚙️ Configura</h1>
        <div class="config-box">
            <h3>Parametri di trading</h3>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
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
            <input type="text" id="video_link_input" placeholder="Incolla link qui..." style="width:100%; padding:10px; margin-bottom:10px;">
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <button class="btn" onclick="analyzeVideo()">▶️ Analizza Ora</button>
                <button class="btn" style="background:#ff9800;" onclick="testVideoForce()">▶️ Test Forza</button>
                <button class="btn" style="background:#4caf50;" onclick="leggiReportVideo()">📄 Report</button>
            </div>
            <div id="video_status" style="margin-top:10px; color:#78828c;">Stato: in attesa di analisi</div>
        </div>

        <div class="config-box">
            <h3>📋 Strategy Tester (link generico)</h3>
            <input type="text" id="strategy_link" placeholder="Incolla link qui..." style="width:100%; padding:10px; margin-bottom:10px;">
            <button class="btn" onclick="testStrategy()">🚀 Avvia Test</button>
            <button class="btn" style="background:#4caf50;" onclick="leggiReport()">📄 Leggi Report</button>
            <button class="btn" style="background:#ff9800;" onclick="applicaStrategia()">✅ Applica</button>
        </div>

        <div class="config-box">
            <h3>🔍 Audit Azienda</h3>
            <button class="btn" onclick="runAudit()">🔎 Esegui Audit</button>
            <button class="btn" style="background:#4caf50;" onclick="leggiAudit()">📄 Leggi Report</button>
            <div id="audit_result" style="margin-top:10px; color:#00c853; font-family:monospace; white-space:pre-wrap; background:#000; padding:10px; border-radius:4px;"></div>
        </div>

        <div class="config-box">
            <h3>Log di sistema</h3>
            <div class="log-box" id="log_box">{{ log }}</div>
            <button class="btn" style="margin-top:10px;" onclick="refreshLog()">Aggiorna Log</button>
        </div>
    </div>
</div>

<script>
    function showSection(id) {
        document.querySelectorAll('.section').forEach(el => el.classList.remove('active'));
        document.getElementById('section-' + id).classList.add('active');
    }

    function fetchStatus() {
        const logDiv = document.getElementById('status_log');
        logDiv.innerText = '📡 Richiesta in corso...';
        fetch('/status')
        .then(r => r.json())
        .then(data => {
            logDiv.innerText = '📡 Aggiornato: ' + new Date().toLocaleTimeString();
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
        })
        .catch(err => {
            logDiv.innerText = '❌ Errore: ' + err;
        });
    }

    function emergencyStop() {
        if (confirm('SEI SICURO?')) {
            fetch('/emergency', { method: 'POST' })
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

    function placeOrder(action) {
        const lots = parseFloat(document.getElementById('order_lots').value);
        const sl = parseFloat(document.getElementById('order_sl').value);
        const tp = parseFloat(document.getElementById('order_tp').value);
        fetch('/place_order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: action, lots: lots, sl: sl, tp: tp})
        })
        .then(r => r.json())
        .then(d => alert(d.message));
    }

    function saveConfig() {
        const session = document.getElementById('session_select').value;
        fetch('/config', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                timeframe: document.getElementById('tf_select').value,
                lot: parseFloat(document.getElementById('lot_input').value),
                session: session
            })
        })
        .then(r => r.json())
        .then(d => alert(d.message));
    }

    function analyzeVideo() {
        const link = document.getElementById('video_link_input').value;
        if (!link) { alert('Inserisci un link'); return; }
        document.getElementById('video_status').innerHTML = 'Stato: 🔄 Analisi in corso...';
        fetch('/analyze_video', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({link: link})
        })
        .then(r => r.json())
        .then(d => {
            alert(d.message);
            fetchVideoStatus();
        });
    }

    function testVideoForce() {
        const link = document.getElementById('video_link_input').value;
        if (!link) { alert('Inserisci un link'); return; }
        document.getElementById('video_status').innerHTML = 'Stato: 🔄 Test forzato in corso...';
        fetch('/test_video_force', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({link: link})
        })
        .then(r => r.json())
        .then(d => {
            alert(d.message);
            setTimeout(fetchVideoStatus, 2000);
        })
        .catch(err => {
            document.getElementById('video_status').innerHTML = 'Stato: ❌ Errore';
        });
    }

    function fetchVideoStatus() {
        fetch('/video_status')
        .then(r => r.json())
        .then(data => {
            if (data.report) {
                document.getElementById('video_status').innerHTML = 'Stato: ✅ Ultima analisi alle ' + data.timestamp;
            } else {
                document.getElementById('video_status').innerHTML = 'Stato: ⏳ Nessun report';
            }
        });
    }

    function leggiReportVideo() {
        fetch('/leggi_report_video')
        .then(r => r.text())
        .then(text => {
            if (text.trim().length === 0) { alert('Nessun report'); return; }
            const win = window.open('', '_blank');
            win.document.write('<pre style="background:#0b0e14; color:#00c853; padding:20px;">' + text + '</pre>');
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
            if (text.trim().length === 0) { alert('Nessun report'); return; }
            const win = window.open('', '_blank');
            win.document.write('<pre style="background:#0b0e14; color:#00c853; padding:20px;">' + text + '</pre>');
        });
    }

    function applicaStrategia() {
        fetch('/applica_strategia', { method: 'POST' })
        .then(r => r.json())
        .then(d => alert(d.message));
    }

    function refreshLog() {
        fetch('/log')
        .then(r => r.text())
        .then(text => document.getElementById('log_box').innerText = text);
    }

    function runAudit() {
        const div = document.getElementById('audit_result');
        div.innerText = '⏳ Esecuzione audit...';
        fetch('/run_audit', { method: 'POST' })
        .then(r => r.text())
        .then(text => {
            div.innerText = text;
        })
        .catch(err => {
            div.innerText = '❌ Errore: ' + err;
        });
    }

    function leggiAudit() {
        const div = document.getElementById('audit_result');
        fetch('/leggi_audit')
        .then(r => r.text())
        .then(text => {
            div.innerText = text;
        })
        .catch(err => {
            div.innerText = '❌ Errore: ' + err;
        });
    }

    // Avvio automatico
    document.addEventListener('DOMContentLoaded', function() {
        fetchStatus();
        fetchVideoStatus();
        setInterval(fetchStatus, 10000);
    });
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
    # Leggi audit_status.json e forza audit se has_issue
    try:
        with open(AUDIT_JSON, 'r') as f:
            fresh_audit = json.load(f)
        if fresh_audit.get('has_issue', False):
            subprocess.run(["python3", "/home/carlo/AI_Trading/audit_agent.py"],
                           capture_output=True, cwd="/home/carlo/AI_Trading")
            with open(AUDIT_JSON, 'r') as f:
                fresh_audit = json.load(f)
    except:
        fresh_audit = audit_data
    return render_template_string(HTML, orders=orders, log=log, now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), agents=AGENTS, audit_data=fresh_audit)

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
    return jsonify({'message': '🛑 SISTEMA FERMATO'})

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

@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    data = request.json
    link = data.get('link')
    if not link:
        return jsonify({'message': 'Link mancante'}), 400
    with open('/home/carlo/AI_Trading/video_link.txt', 'w') as f:
        f.write(link)
    with open('/home/carlo/video_analysis.log', 'w') as log:
        subprocess.Popen(["python3", "/home/carlo/AI_Trading/multidigest.py"],
                         stdout=log, stderr=log,
                         cwd="/home/carlo/AI_Trading")
    return jsonify({'message': f'Analisi avviata per: {link}. Controlla report_multivideo.txt tra qualche minuto.'})

@app.route('/test_video_force', methods=['POST'])
def test_video_force():
    link = request.json.get('link')
    if not link:
        return jsonify({'message': 'Link mancante'}), 400
    with open('/home/carlo/AI_Trading/video_link.txt', 'w') as f:
        f.write(link)
    subprocess.Popen(
        ["python3", "/home/carlo/AI_Trading/multidigest.py", "--force"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd="/home/carlo/AI_Trading"
    )
    return jsonify({'message': f'Test forzato avviato per {link}'})

@app.route('/video_status')
def video_status():
    report_path = '/home/carlo/AI_Trading/report_multivideo.txt'
    try:
        with open(report_path, 'r') as f:
            content = f.read()
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

@app.route('/run_audit', methods=['POST'])
def run_audit():
    result = subprocess.run(["python3", "/home/carlo/AI_Trading/audit_agent.py"],
                            capture_output=True, text=True, cwd="/home/carlo/AI_Trading")
    if result.returncode == 0:
        try:
            with open('/home/carlo/AI_Trading/audit_report.txt', 'r') as f:
                return f.read()
        except:
            return "Report generato ma non leggibile."
    else:
        return f"Errore: {result.stderr}"

@app.route('/leggi_audit')
def leggi_audit():
    try:
        with open('/home/carlo/AI_Trading/audit_report.txt', 'r') as f:
            return f.read()
    except:
        return "Nessun report audit disponibile."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
