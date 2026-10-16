import sys, os
sys.path.insert(0, '.')
from tools.data_fetcher import DataFetcher

fetcher = DataFetcher()

# Scarica dati per backtest realistico
symbols = ['EURUSD', 'GBPUSD', 'XAUUSD', 'NAS100']
for sym in symbols:
    print(f"Scaricando {sym}...")
    fetcher.fetch_multi_timeframe(sym, intervals=['15min','60min','4h','daily'])

print("✅ Dati scaricati per tutti i simboli e timeframe.")
