from flask import Flask, jsonify, render_template_string
import json, os
from datetime import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html><head><title>AI_BRIDGE Dashboard</title>
<style>body{font-family:Arial;padding:20px;background:#f4f4f4;} table{border-collapse:collapse;width:100%} td,th{border:1px solid #ddd;padding:8px;} th{background:#4CAF50;color:#fff;}
</style></head>
<body>
<h1>🤖 AI_BRIDGE V3 - FP Markets</h1>
<p>Ultimo aggiornamento: {{ time }}</p>
<h2>📊 Posizioni Aperte</h2>
<table><tr><th>Simbolo</th><th>Lotti</th><th>Prezzo</th><th>SL</th><th>TP</th><th>PNL</th></tr>
{% for p in positions %}
<tr><td>{{ p.symbol }}</td><td>{{ p.volume }}</td><td>{{ p.price_open }}</td><td>{{ p.sl }}</td><td>{{ p.tp }}</td><td>{{ p.profit }}</td></tr>
{% endfor %}
</table>
<h2>📈 Ordini Recenti</h2>
<table><tr><th>Az.</th><th>Lotti</th><th>Prezzo</th><th>SL</th><th>TP</th><th>Ora</th></tr>
{% for o in orders[-10:] %}
<tr><td>{{ o.action }}</td><td>{{ o.lots }}</td><td>{{ o.price }}</td><td>{{ o.sl }}</td><td>{{ o.tp }}</td><td>{{ o.time|int|timestamp }}</td></tr>
{% endfor %}
</table>
</body>
</html>
"""

@app.template_filter('timestamp')
def timestamp_filter(s):
    return datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    orders = []
    positions = []
    orders_file = os.path.expanduser('~/mt4_shared/orders.json')
    if os.path.exists(orders_file):
        with open(orders_file) as f:
            orders = json.load(f)
    return render_template_string(HTML, orders=orders, positions=positions, time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
