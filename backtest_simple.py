import pandas as pd
import json
import numpy as np

data = pd.read_csv('data/historical/GBP_USD_15min.csv', index_col=0, parse_dates=True)
data = data[['Open','High','Low','Close']]
data = data.sort_index()

data['pattern'] = 0
for i in range(2, len(data)):
    c1, c2, c3 = data.Close.iloc[i-2:i+1]
    o1, o2, o3 = data.Open.iloc[i-2:i+1]
    if c1 > o1 and c2 > o2 and c3 > o3:
        data.loc[data.index[i], 'pattern'] = 1
    elif c1 < o1 and c2 < o2 and c3 < o3:
        data.loc[data.index[i], 'pattern'] = -1

data['range'] = data.High - data.Low
data['atr'] = data['range'].rolling(14).mean()
data = data.dropna(subset=['atr'])

capital = 10000
risk = 0.02
sl_ratio = 1.5
tp_ratio = 1.5

trades = []
position = 0
entry_price = 0
sl = 0
tp = 0

for i in range(3, len(data)):
    if position == 0 and data.pattern.iloc[i] != 0:
        bias = data.pattern.iloc[i]
        price = data.Close.iloc[i]
        atr = data.atr.iloc[i]
        if np.isnan(atr) or atr == 0:
            continue
        sl = price - sl_ratio * atr if bias == 1 else price + sl_ratio * atr
        tp = price + tp_ratio * abs(price - sl) if bias == 1 else price - tp_ratio * abs(price - sl)
        size = int(capital * risk / (abs(price - sl) + 0.0001))
        if size == 0:
            size = 1
        entry_price = price
        position = bias
        trades.append({'time': data.index[i], 'bias': bias, 'entry': price, 'sl': sl, 'tp': tp, 'size': size, 'exit': None, 'pnl': 0})
    elif position != 0:
        price = data.Close.iloc[i]
        if position == 1:
            if price <= sl or price >= tp:
                pnl = (price - entry_price) * size / 100000 * 10000
                capital += pnl
                trades[-1]['exit'] = price
                trades[-1]['pnl'] = pnl
                position = 0
        else:
            if price >= sl or price <= tp:
                pnl = (entry_price - price) * size / 100000 * 10000
                capital += pnl
                trades[-1]['exit'] = price
                trades[-1]['pnl'] = pnl
                position = 0

print(f"Capitale finale: {capital:.2f}")
print(f"Totale trades: {len(trades)}")
for t in trades:
    print(f"{t['time']} {t['bias']} entry {t['entry']:.5f} exit {t.get('exit', 'open')} PNL {t.get('pnl', 0):.2f}")
