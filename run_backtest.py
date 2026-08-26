import sys, yfinance as yf, backtrader as bt
sys.path.insert(0, ".")
from strategies.three_candles import ThreeCandles

data = yf.download('EURUSD=X', start='2026-07-01', end='2026-08-20', multi_level_index=False)
data.columns = ['Open','High','Low','Close','Volume']

cerebro = bt.Cerebro()
cerebro.adddata(bt.feeds.PandasData(dataname=data))
cerebro.addstrategy(ThreeCandles)
cerebro.broker.set_cash(10000)
cerebro.addsizer(bt.sizers.PercentSizer, percents=2)

print('Capitale iniziale:', cerebro.broker.getvalue())
cerebro.run()
print('Capitale finale:', cerebro.broker.getvalue())
