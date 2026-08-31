import yfinance as yf
import time, os
from datetime import datetime

def get_volume_anomaly():
    try:
        df = yf.download("EURUSD=X", period="1d", interval="5m", progress=False)
        if df.empty:
            return {"ratio": 1.0, "anomaly": False}
        avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
        last_volume = df['Volume'].iloc[-1]
        ratio = last_volume / avg_volume if avg_volume > 0 else 1
        # Punteggio: >1.5 → +0.3, <0.5 → -0.3, altrimenti 0
        if ratio > 1.5:
            score = 0.3
        elif ratio < 0.5:
            score = -0.3
        else:
            score = 0.0
        return {
            "ratio": ratio,
            "anomaly": ratio > 1.5,
            "score": score,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"ratio": 1.0, "anomaly": False, "score": 0.0, "timestamp": datetime.now().isoformat()}

while True:
    data = get_volume_anomaly()
    with open("/home/carlo/AI_Trading/volume_context.txt", "w") as f:
        f.write(f"Timestamp: {data['timestamp']}\n")
        f.write(f"Volume ratio: {data['ratio']:.2f}\n")
        f.write(f"Anomaly: {data['anomaly']}\n")
        f.write(f"Punteggio: {data['score']:.2f}\n")
    print(f"Volume aggiornato: ratio {data['ratio']:.2f}, score {data['score']:.2f}")
    time.sleep(300)
