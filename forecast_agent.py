#!/usr/bin/env python3
"""forecast_agent.py - Usa TimesFM 2.5 per prevedere EURUSD (M15)."""
import os, json, time
import numpy as np
import yfinance as yf
from datetime import datetime

OUTPUT_JSON = "/home/carlo/AI_Trading/forecast.json"

def main():
    try:
        # 1. Scarica ultimi 100 prezzi M15
        df = yf.download("EURUSD=X", period="2d", interval="15m", progress=False)
        if df.empty or len(df) < 50:
            print("[forecast] Dati insufficienti.", flush=True)
            return
            
        # Appiattisci MultiIndex se presente
        if hasattr(df.columns, "get_level_values"):
            df.columns = df.columns.get_level_values(0)
            
        close = df["Close"].dropna().values
        last_price = float(close[-1])
        
        # 2. Carica TimesFM
        import timesfm
        model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
        model.compile(
            timesfm.ForecastConfig(
                max_context=512,
                max_horizon=12,
                normalize_inputs=True,
                use_continuous_quantile_head=True,
            )
        )
        
        # 3. Calcola forecast
        # Prendi gli ultimi 100 punti
        serie = close[-100:]
        point, _ = model.forecast(horizon=12, inputs=[serie])
        
        forecast_price = float(point[0][-1])  # Prezzo tra 12 step (3 ore)
        delta_pct = (forecast_price - last_price) / last_price * 100
        
        if delta_pct > 0.05:
            direction = "BULLISH"
        elif delta_pct < -0.05:
            direction = "BEARISH"
        else:
            direction = "NEUTRAL"
            
        result = {
            "timestamp": datetime.now().isoformat(),
            "last_price": round(last_price, 5),
            "forecast_price": round(forecast_price, 5),
            "delta_pct": round(delta_pct, 3),
            "direction": direction
        }
        
        with open(OUTPUT_JSON, "w") as f:
            json.dump(result, f, indent=2)
            
        print(f"[forecast] {direction} (delta {delta_pct:+.3f}%)", flush=True)
        
    except Exception as e:
        print(f"[forecast] Errore: {e}", flush=True)

if __name__ == "__main__":
    main()
