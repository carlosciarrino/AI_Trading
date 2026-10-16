from flask import Flask, render_template_string, jsonify
import json, os, subprocess
from datetime import datetime

app = Flask(__name__)

AGENTS = ["ai_workforce", "dashboard", "sentinel", "news_agent", "social_agent", "cycle_agent", "experience_agent", "strategy_tester_agent", "github_researcher", "skill_researcher", "news_critical", "ai_researcher_agent", "ai_tester_agent", "sync_agent"]

def get_status():
    out = subprocess.run(["tmux", "ls"], capture_output=True, text=True)
    sessions = out.stdout if out.returncode == 0 else ""
    status = {a: "active" if a in sessions else "stopped" for a in AGENTS}
    return status

HTML = """
<!DOCTYPE html>
<html>
<head><title>AI_BRIDGE minimal</title></head>
<body>
<h1>AI_BRIDGE V5 (minimal)</h1>
<button onclick="fetchStatus()">Aggiorna stato</button>
<pre id="status"></pre>
<script>
function fetchStatus() {
    fetch('/status')
    .then(r => r.json())
    .then(data => {
        document.getElementById('status').innerText = JSON.stringify(data, null, 2);
    });
}
fetchStatus();
setInterval(fetchStatus, 5000);
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/status')
def status():
    return jsonify(get_status())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
