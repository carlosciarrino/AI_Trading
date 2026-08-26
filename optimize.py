import pandas as pd
import numpy as np
from itertools import product

data = pd.read_csv('data/historical/EUR_USD_15min.csv', index_col=0, parse_dates=True)
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
data = data.dropna()

def backtest(sl_ratio, tp_ratio, risk=0.02):
    capital = 10000
    position = 0
    for i in range(3, len(data)):
        if position == 0 and data.pattern.iloc[i] != 0:
            bias = data.pattern.iloc[i]
            price = data.Close.iloc[i]
            atr = data.atr.iloc[i]
            if np.isnan(atr) or atr == 0: continue
            sl = price - sl_ratio * atr if bias == 1 else price + sl_ratio * atr
            tp = price + tp_ratio * abs(price - sl) if bias == 1 else price - tp_ratio * abs(price - sl)
            size = int(capital * risk / (abs(price - sl) + 0.0001))
            if size == 0: size = 1
            entry_price = price
            position = bias
        elif position != 0:
            price = data.Close.iloc[i]
            if position == 1:
                if price <= sl or price >= tp:
                    capital += (price - entry_price) * size / 100000 * 10000
                    position = 0
            else:
                if price >= sl or price <= tp:
                    capital += (entry_price - price) * size / 100000 * 10000
                    position = 0
    return capital

best = {'sl': 0, 'tp': 0, 'capital': 0}
for sl, tp in product([1.0, 1.2, 1.5, 2.0, 2.5], [1.0, 1.2, 1.5, 2.0, 2.5]):
    cap = backtest(sl, tp)
    print(f"SL {sl} TP {tp} -> {cap:.2f}")
    if cap > best['capital']:
        best = {'sl': sl, 'tp': tp, 'capital': cap}

print(f"\n🏆 BEST: SL {best['sl']} TP {best['tp']} -> {best['capital']:.2f}")
