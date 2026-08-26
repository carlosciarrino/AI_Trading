import json, os, pandas as pd, plotly.graph_objects as go
from datetime import datetime

def generate():
    orders_file = os.path.expanduser('~/mt4_shared/orders.json')
    if not os.path.exists(orders_file):
        return
    with open(orders_file) as f:
        orders = json.load(f)
    if not orders:
        return

    df = pd.DataFrame(orders)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df.sort_values('time')

    # Equity curve
    df['equity'] = 10000 + df['pnl'].fillna(0).cumsum() if 'pnl' in df else 10000

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time'], y=df['equity'], mode='lines', name='Equity'))
    fig.update_layout(title='Equity Curve', xaxis_title='Time', yaxis_title='Equity')

    html = fig.to_html()
    with open('dashboard_advanced.html', 'w') as f:
        f.write(html)
    print("✅ Dashboard avanzata generata in dashboard_advanced.html")

if __name__ == '__main__':
    generate()
