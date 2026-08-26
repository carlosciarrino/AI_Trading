import os, json, time, requests, pandas as pd
from datetime import datetime, timedelta

API_KEY = "a84607a207f34d2780a671dec15d842c"
BASE_URL = "https://api.twelvedata.com"

SYMBOLS = ["EUR/USD", "GBP/USD"]
INTERVALS = ["5min", "15min", "1h", "4h"]
OUTPUT_SIZE = 5000  # massimo per chiamata

data_dir = os.path.expanduser("~/AI_Trading/data/historical")
os.makedirs(data_dir, exist_ok=True)

for symbol in SYMBOLS:
    for interval in INTERVALS:
        print(f"Scaricando {symbol} {interval}...")
        url = f"{BASE_URL}/time_series"
        params = {
            "symbol": symbol,
            "interval": interval,
            "outputsize": OUTPUT_SIZE,
            "apikey": API_KEY
        }
        try:
            r = requests.get(url, params=params, timeout=30)
            if r.status_code != 200:
                print(f"  ❌ Errore HTTP {r.status_code}: {r.text[:200]}")
                continue
            data = r.json()
            if "values" not in data:
                print(f"  ❌ Errore API: {data.get('message', 'Unknown error')}")
                continue
            df = pd.DataFrame(data["values"])
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df.set_index("datetime")
            df = df.astype(float)
            df = df[["open", "high", "low", "close"]]
            df.columns = ["Open", "High", "Low", "Close"]
            # Salva
            fname = f"{symbol.replace('/','_')}_{interval}.csv"
            fpath = os.path.join(data_dir, fname)
            df.to_csv(fpath)
            print(f"  ✅ Salvato {len(df)} righe in {fpath}")
            time.sleep(1.5)  # rispetta il rate limit (8/minuto)
        except Exception as e:
            print(f"  ❌ Errore: {e}")
