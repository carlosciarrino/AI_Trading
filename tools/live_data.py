import os, json, requests, pandas as pd
from datetime import datetime, timedelta

API_KEY = "a84607a207f34d2780a671dec15d842c"
BASE_URL = "https://api.twelvedata.com"

def get_recent(symbol="EUR/USD", interval="15min", length=10):
    url = f"{BASE_URL}/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": length,
        "apikey": API_KEY
    }
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    if "values" not in data:
        raise Exception(f"Errore Twelve Data: {data}")
    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime")
    df = df[["open", "high", "low", "close"]]
    df.columns = ["Open", "High", "Low", "Close"]
    df = df.astype(float)
    return df

if __name__ == "__main__":
    print(get_recent().tail())

def get_recent_yahoo(symbol="EURUSD=X", interval="1d", length=50):
    import yfinance as yf
    import pandas as pd
    df = yf.download(symbol, period="60d", interval=interval, multi_level_index=False)
    if df.empty:
        raise Exception("Nessun dato da Yahoo")
    df = df[['Open','High','Low','Close']].tail(length)
    return df
