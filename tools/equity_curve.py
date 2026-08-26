import pandas as pd, json, os, plotly.graph_objects as go
from datetime import datetime

def generate_equity_curve():
    orders_file = os.path.expanduser('~/mt4_shared/orders.json')
    if not os.path.exists(orders_file):
        return
    with open(orders_file) as f:
        orders = json.load(f)
    if not orders:
        return

    # Normalizza: calcola PNL se manca
    for o in orders:
        if 'pnl' not in o and o.get('status') == 'closed' and o.get('close_price'):
            entry = o.get('price', 1.0)
            close = o.get('close_price', entry)
            lots = o.get('lots', 0.01)
            pnl = (close - entry) * lots * 100000 if o.get('action') == 'buy' else (entry - close) * lots * 100000
            o['pnl'] = round(pnl, 2)
        elif 'pnl' not in o:
            o['pnl'] = 0

    df = pd.DataFrame(orders)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df.sort_values('time')
    df['cum_pnl'] = df['pnl'].fillna(0).cumsum()
    df['equity'] = 10000 + df['cum_pnl']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time'], y=df['equity'], mode='lines', name='Equity', line=dict(color='#2962ff')))
    fig.update_layout(title='Equity Curve', xaxis_title='Data', yaxis_title='Capitale', template='plotly_dark', height=400)
    os.makedirs('/home/carlo/AI_Trading/static', exist_ok=True)
    fig.write_html('/home/carlo/AI_Trading/static/equity.html')
    print("✅ Equity curve generata")

if __name__ == '__main__':
    generate_equity_curve()
