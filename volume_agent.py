import yfinance as yf
import time, os
from datetime import datetime

def get_volume_anomaly():
    df = yf.download("EURUSD=X", period="1d", interval="5m", progress=False)
    avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
    last_volume = df['Volume'].iloc[-1]
    ratio = last_volume / avg_volume if avg_volume > 0 else 1
    return {"ratio": ratio, "anomaly": ratio > 1.5, "timestamp": datetime.now().isoformat()}

while True:
    data = get_volume_anomaly()
    with open("/home/carlo/AI_Trading/volume_context.txt", "w") as f:
        f.write(f"Volume ratio: {data['ratio']:.2f}\nAnomaly: {data['anomaly']}")
    time.sleep(300)
