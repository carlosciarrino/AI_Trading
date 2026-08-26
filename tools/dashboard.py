import os, json, time, glob
from datetime import datetime

def generate_dashboard():
    orders_file = os.path.expanduser('~/mt4_shared/orders.json')
    orders = []
    if os.path.exists(orders_file):
        with open(orders_file) as f:
            orders = json.load(f)

    html = f"""<!DOCTYPE html>
<html>
<head><title>AI Trading Dashboard</title>
<style>
body {{ font-family: Arial; margin: 40px; background: #f4f4f4; }}
table {{ border-collapse: collapse; width: 100%; background: white; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #4CAF50; color: white; }}
.metric {{ display: inline-block; margin: 20px; padding: 20px; background: white; border-radius: 10px; }}
</style>
</head>
<body>
    <h1>📊 AI Trading Dashboard</h1>
    <p>Ultimo aggiornamento: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <div class="metric">Ordini totali: {len(orders)}</div>
    <div class="metric">Ultimo segnale: {orders[-1].get('action', 'N/A') if orders else 'N/A'}</div>
    <table>
        <tr><th>#</th><th>Azione</th><th>Lotti</th><th>Prezzo</th><th>SL</th><th>TP</th><th>Orario</th></tr>
        {''.join([f"<tr><td>{i+1}</td><td>{o.get('action','')}</td><td>{o.get('lots','')}</td><td>{o.get('price','')}</td><td>{o.get('sl','')}</td><td>{o.get('tp','')}</td><td>{o.get('time','')}</td></tr>" for i, o in enumerate(orders[-20:])])}
    </table>
</body>
</html>
"""
    with open('dashboard.html', 'w') as f:
        f.write(html)
    print("✅ Dashboard generata in dashboard.html")

if __name__ == "__main__":
    generate_dashboard()
