import sys, pandas as pd, backtrader as bt
sys.path.insert(0, ".")
from strategies.three_candles import ThreeCandles

# Carica dati scaricati da Alpha Vantage
data_dir = "data/historical"
df = pd.read_csv(f'{data_dir}/EURUSD_15min_20260820.csv', index_col=0, parse_dates=True)
df = df[['Open','High','Low','Close']]

cerebro = bt.Cerebro()
cerebro.adddata(bt.feeds.PandasData(dataname=df))
cerebro.addstrategy(ThreeCandles)
cerebro.broker.set_cash(10000)
cerebro.addsizer(bt.sizers.PercentSizer, percents=2)

print('Capitale iniziale:', cerebro.broker.getvalue())
cerebro.run()
print('Capitale finale:', cerebro.broker.getvalue())
