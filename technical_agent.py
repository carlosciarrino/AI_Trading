#!/usr/bin/env python3
"""technical_agent.py - Calcola indicatori tecnici (EMA, RSI, ADX, OBV).
Scrive technical_context.txt per log/analisi. Peso 0 nell'orchestratore.
Basato su technical-basic di Vibe-Trading (pandas puro).
"""
import yfinance as yf
import json
import pandas as pd
import numpy as np
import time, os
from datetime import datetime

CONTEXT_PATH = "/home/carlo/AI_Trading/technical_context.txt"

VOLUME_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/volume_data.json"


def load_real_volume():
    try:
        with open(VOLUME_JSON) as f:
            return json.load(f).get("volume", 0)
    except:
        return 0



def compute_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)


def compute_adx(high, low, close, period=14):
    prev_high = high.shift(1)
    prev_low = low.shift(1)
    prev_close = close.shift(1)
    up_move = high - prev_high
    down_move = prev_low - low
    plus_dm = pd.Series(0.0, index=high.index)
    minus_dm = pd.Series(0.0, index=high.index)
    plus_dm[(up_move > down_move) & (up_move > 0)] = up_move
    minus_dm[(down_move > up_move) & (down_move > 0)] = down_move
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    alpha = 1 / period
    smoothed_tr = tr.ewm(alpha=alpha, min_periods=period).mean()
    smoothed_plus_dm = plus_dm.ewm(alpha=alpha, min_periods=period).mean()
    smoothed_minus_dm = minus_dm.ewm(alpha=alpha, min_periods=period).mean()
    plus_di = 100 * smoothed_plus_dm / smoothed_tr
    minus_di = 100 * smoothed_minus_dm / smoothed_tr
    di_sum = plus_di + minus_di
    di_sum = di_sum.replace(0, np.nan)
    dx = 100 * (plus_di - minus_di).abs() / di_sum
    adx = dx.ewm(alpha=alpha, min_periods=period).mean()
    return pd.DataFrame({"plus_di": plus_di, "minus_di": minus_di, "adx": adx})


def compute_bollinger(close, window=20, num_std=2.0):
    mid = close.rolling(window).mean()
    std = close.rolling(window).std()
    return pd.DataFrame({
        "bb_mid": mid,
        "bb_upper": mid + num_std * std,
        "bb_lower": mid - num_std * std,
    })


def compute_obv(close, volume):
    sign = close.diff().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    return (volume * sign).cumsum()


def compute_signal(df):
    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    real_vol = load_real_volume()
    if real_vol > 0:
        volume = pd.Series([real_vol] * len(df), index=df.index)
    else:
        volume = df["Volume"]

    # Trend
    ema_f = close.ewm(span=9, adjust=False).mean()
    ema_s = close.ewm(span=21, adjust=False).mean()
    adx_df = compute_adx(high, low, close, 14)
    adx = adx_df["adx"].iloc[-1]
    trend_bull = ema_f.iloc[-1] > ema_s.iloc[-1] and adx > 20
    trend_bear = ema_f.iloc[-1] < ema_s.iloc[-1] and adx > 20

    # Mean reversion
    bb = compute_bollinger(close, 20, 2.0)
    rsi = compute_rsi(close, 14)
    close_now = close.iloc[-1]
    rsi_now = rsi.iloc[-1]
    mr_oversold = close_now < bb["bb_lower"].iloc[-1] and rsi_now < 30
    mr_overbought = close_now > bb["bb_upper"].iloc[-1] and rsi_now > 70

    # Volume
    obv = compute_obv(close, volume)
    obv_ma = obv.rolling(20).mean()
    vol_bull = obv.iloc[-1] > obv_ma.iloc[-1]
    vol_bear = obv.iloc[-1] < obv_ma.iloc[-1]

    # Voto
    buy = (trend_bull or mr_oversold) and vol_bull and not mr_overbought
    sell = (trend_bear or mr_overbought) and vol_bear and not mr_oversold

    if buy:
        signal = 1
        direction = "LONG"
    elif sell:
        signal = -1
        direction = "SHORT"
    else:
        signal = 0
        direction = "STAND_ASIDE"

    return {
        "signal": signal,
        "direction": direction,
        "ema_fast": round(ema_f.iloc[-1], 5),
        "ema_slow": round(ema_s.iloc[-1], 5),
        "adx": round(float(adx), 2),
        "rsi": round(float(rsi_now), 2),
        "bb_upper": round(bb["bb_upper"].iloc[-1], 5),
        "bb_lower": round(bb["bb_lower"].iloc[-1], 5),
        "close": round(close_now, 5),
        "obv": round(float(obv.iloc[-1]), 2),
        "obv_ma": round(float(obv_ma.iloc[-1]), 2),
        "trend_bull": trend_bull,
        "trend_bear": trend_bear,
        "mr_oversold": mr_oversold,
        "mr_overbought": mr_overbought,
        "vol_bull": vol_bull,
        "vol_bear": vol_bear,
    }


def process():
    try:
        df = yf.download("EURUSD=X", period="5d", interval="15m", progress=False)
        if df.empty:
            print("[technical] Nessun dato", flush=True)
            return
        # Appiattisci MultiIndex se presente
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if len(df) < 30:
            print(f"[technical] Poche candele ({len(df)})", flush=True)
            return

        res = compute_signal(df)

        with open(CONTEXT_PATH, "w") as f:
            f.write(f"Technical (aggiornato {datetime.now().isoformat()}):\n")
            f.write(f"Signal: {res['direction']}\n")
            f.write(f"Close: {res['close']}\n")
            f.write(f"EMA9: {res['ema_fast']} | EMA21: {res['ema_slow']}\n")
            f.write(f"ADX: {res['adx']}\n")
            f.write(f"RSI: {res['rsi']}\n")
            f.write(f"BB: {res['bb_lower']} - {res['bb_upper']}\n")
            f.write(f"OBV: {res['obv']} | OBV_MA: {res['obv_ma']}\n")
            f.write(f"Trend: bull={res['trend_bull']} bear={res['trend_bear']}\n")
            f.write(f"MR: oversold={res['mr_oversold']} overbought={res['mr_overbought']}\n")
            f.write(f"Volume: bull={res['vol_bull']} bear={res['vol_bear']}\n")
            f.write(f"Punteggio: 0.00\n")

        print(f"[technical] {res['direction']} (RSI {res['rsi']}, ADX {res['adx']})", flush=True)
    except Exception as e:
        print(f"[technical] Errore: {e}", flush=True)


if __name__ == "__main__":
    while True:
        process()
        time.sleep(900)  # 15 min
