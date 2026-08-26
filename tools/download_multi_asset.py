import os, time, requests, pandas as pd
from datetime import datetime

SYMBOLS = {
    'GBPUSD': 'GBP/USD',
    'XAUUSD': 'XAU/USD',
    'US100': 'US100'
}
INTERVAL = "15min"
API_KEY = "a84607a207f34d2780a671dec15d842c"
BASE_URL = "https://api.twelvedata.com"

data_dir = os.path.expanduser("~/AI_Trading/data/historical")
os.makedirs(data_dir, exist_ok=True)

for name, symbol in SYMBOLS.items():
    print(f"📥 Scaricando {name}...")
    url = f"{BASE_URL}/time_series"
    params = {
        "symbol": symbol,
        "interval": INTERVAL,
        "outputsize": 5000,
        "apikey": API_KEY
    }
    try:
        r = requests.get(url, params=params, timeout=30)
        if r.status_code != 200:
            print(f"  ❌ Errore {r.status_code}: {r.text[:100]}")
            continue
        data = r.json()
        if "values" not in data:
            print(f"  ❌ Nessun dato per {symbol}")
            continue
        df = pd.DataFrame(data["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.set_index("datetime")
        df = df[["open", "high", "low", "close"]]
        df.columns = ["Open", "High", "Low", "Close"]
        df = df.astype(float)
        fname = f"{name}_{INTERVAL}.csv"
        df.to_csv(os.path.join(data_dir, fname))
        print(f"  ✅ Salvato {len(df)} righe per {name}")
        time.sleep(1.5)
    except Exception as e:
        print(f"  ❌ Errore: {e}")
