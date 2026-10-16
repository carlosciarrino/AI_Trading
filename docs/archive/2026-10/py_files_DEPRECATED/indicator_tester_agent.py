import yfinance as yf
import pandas as pd
import numpy as np
import time, os
from datetime import datetime

REPORT_PATH = os.path.expanduser("~/AI_Trading/report_indicatori.txt")

def is_night():
    h = datetime.now().hour
    return h >= 22 or h < 6

def backtest():
    if not is_night():
        print("Orario diurno. Backtest solo notturno.", flush=True)
        return
    try:
        df = yf.download("EURUSD=X", period="1y", interval="1h", progress=False)
        if df.empty:
            return
        df['SMA20'] = df['Close'].rolling(20).mean()
        df['SMA50'] = df['Close'].rolling(50).mean()
        df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().rolling(14).mean() / df['Close'].pct_change().rolling(14).std()))
        df['Signal'] = 0
        df.loc[df['SMA20'] > df['SMA50'], 'Signal'] = 1
        df.loc[df['SMA20'] < df['SMA50'], 'Signal'] = -1
        df['Return'] = df['Close'].pct_change() * df['Signal'].shift(1)
        total_return = df['Return'].sum() * 100
        wins = (df['Return'] > 0).sum()
        losses = (df['Return'] < 0).sum()
        win_rate = wins / (wins + losses) if (wins+losses)>0 else 0
        report = f"""Report Backtest - {datetime.now()}
Periodo: ultimo anno (orario)
Ritorno: {total_return:.2f}%
Vincite: {wins}, Perdite: {losses}
Win Rate: {win_rate:.2%}
Indicatori: SMA20, SMA50, RSI(14)
Strategia: incrocio SMA
"""
        with open(REPORT_PATH, "w") as f:
            f.write(report)
        print(f"Report indicatori aggiornato (notturno): {total_return:.2f}%", flush=True)
    except Exception as e:
        print(f"Errore backtest: {e}", flush=True)

while True:
    backtest()
    time.sleep(86400)  # una volta al giorno
