import sys, pandas as pd, json
sys.path.insert(0, ".")
from strategies.three_candles_intraday import ThreeCandlesIntraday

ASSETS = ["GBPUSD", "XAUUSD", "NAS100"]
INTERVAL = "15min"
results = {}

for asset in ASSETS:
    fname = f"data/historical/{asset}_{INTERVAL}.csv"
    try:
        df = pd.read_csv(fname, index_col=0, parse_dates=True)
        df = df[['Open','High','Low','Close']]
        print(f"📊 Backtest {asset}... {len(df)} candele")
        # Usa backtrader (come in run_backtest_intraday.py)
        import backtrader as bt
        cerebro = bt.Cerebro()
        cerebro.adddata(bt.feeds.PandasData(dataname=df))
        cerebro.addstrategy(ThreeCandlesIntraday)
        cerebro.broker.set_cash(10000)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=2)
        cerebro.run()
        final = cerebro.broker.getvalue()
        results[asset] = final
        print(f"  ✅ {asset}: 10000 → {final:.2f}")
    except Exception as e:
        print(f"  ❌ {asset}: {e}")

print("\n=== RISULTATI BACKTEST MULTI-ASSET ===")
for asset, val in results.items():
    print(f"{asset}: {val:.2f}")
