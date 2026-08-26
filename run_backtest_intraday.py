import sys, pandas as pd, backtrader as bt
sys.path.insert(0, ".")
from strategies.three_candles_intraday import ThreeCandlesIntraday

data_dir = "data/historical"

# Carica dati M15
df_m15 = pd.read_csv(f'{data_dir}/EUR_USD_15min.csv', index_col=0, parse_dates=True)
df_m15 = df_m15[['Open','High','Low','Close']]

# Carica dati H4 per bias (opzionale)
# df_h4 = pd.read_csv(f'{data_dir}/EUR_USD_4h.csv', index_col=0, parse_dates=True)

cerebro = bt.Cerebro()
cerebro.adddata(bt.feeds.PandasData(dataname=df_m15))
cerebro.addstrategy(ThreeCandlesIntraday)
cerebro.broker.set_cash(10000)
cerebro.addsizer(bt.sizers.PercentSizer, percents=2)

print('Capitale iniziale:', cerebro.broker.getvalue())
cerebro.run()
print('Capitale finale:', cerebro.broker.getvalue())
# cerebro.plot()
