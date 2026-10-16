import os, json, glob
from datetime import datetime

def generate():
    reports = glob.glob("reports/backtest_*.json")
    if not reports:
        print("Nessun report trovato.")
        return
    latest = max(reports, key=os.path.getctime)
    with open(latest, 'r') as f:
        data = json.load(f)

    html = f"""<!DOCTYPE html>
<html><head><title>AI Trading Dashboard</title></head>
<body>
    <h1>📊 Report Backtest - {datetime.today().strftime('%Y-%m-%d')}</h1>
    <p>Trade totali: {data.get('total_trades', 0)}</p>
    <p>Win rate: {data.get('win_rate', 0):.2f}%</p>
    <p>Profit factor: {data.get('profit_factor', 0):.2f}</p>
    <p>Drawdown massimo: {data.get('max_drawdown', 0):.2f}%</p>
    <p>Sharpe ratio: {data.get('sharpe_ratio', 0):.2f}</p>
    <hr>
    <pre>{json.dumps(data, indent=2)}</pre>
</body></html>
"""
    with open("dashboard.html", "w") as f:
        f.write(html)
    print("✅ Dashboard generata in dashboard.html")

if __name__ == "__main__":
    generate()
