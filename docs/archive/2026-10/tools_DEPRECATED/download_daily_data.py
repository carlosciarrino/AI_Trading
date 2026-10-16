import sys, os
import yfinance as yf
import pandas as pd
from datetime import datetime

symbols = ['EURUSD=X', 'GBPUSD=X', 'GC=F', '^IXIC']
data_dir = os.path.expanduser('~/AI_Trading/data/historical')
os.makedirs(data_dir, exist_ok=True)

for sym in symbols:
    print(f"Scaricando {sym}...")
    try:
        df = yf.download(sym, start='2020-01-01', end=datetime.today().strftime('%Y-%m-%d'), multi_level_index=False)
        df = df[['Open','High','Low','Close','Volume']]
        filename = f"{sym.replace('=','').replace('^','')}_daily.csv"
        df.to_csv(os.path.join(data_dir, filename))
        print(f"✅ {sym} salvato")
    except Exception as e:
        print(f"❌ {sym} fallito: {e}")
