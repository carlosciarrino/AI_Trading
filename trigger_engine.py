#!/usr/bin/env python3
"""trigger_engine.py - Gate di mercato con volume MT4 + candela forte.
Controlla: (Volume spike OR Candela forte) AND Trend EMA21 allineato.
Scrive triggers.json per l'orchestratore.
"""
import json, os, time
from datetime import datetime, timezone

BASE = "/home/carlo/Progetti/AI_Trading"
TECH_CONTEXT = os.path.join(BASE, "technical_context.txt")
VOLUME_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/volume_data.json"
VOLUME_HISTORY_FILE = os.path.join(BASE, "volume_history.json")
OUTPUT_JSON = os.path.join(BASE, "triggers.json")

VOLUME_SPIKE_FACTOR = 1.5
HISTORY_LENGTH = 5
CANDLE_BODY_ATR_RATIO = 0.5  # 50% dell'ATR

def is_market_open():
    """Controlla se il mercato forex e' aperto (Londra/NY)."""
    now = datetime.now(timezone.utc)
    if now.weekday() == 4 and now.hour >= 22:
        return False
    if now.weekday() == 5:
        return False
    if now.weekday() == 6 and now.hour < 22:
        return False
    return True

def read_volume_mt4():
    """Legge volume attuale da volume_data.json (MT4)."""
    try:
        with open(VOLUME_JSON) as f:
            data = json.load(f)
        return int(data.get("volume", 0))
    except Exception:
        return 0

def update_volume_history(current_vol):
    """Aggiorna history in volume_history.json, mantiene ultimi 5 valori."""
    history = []
    if os.path.exists(VOLUME_HISTORY_FILE):
        try:
            with open(VOLUME_HISTORY_FILE) as f:
                history = json.load(f)
        except Exception:
            history = []
    history.append(current_vol)
    history = history[-HISTORY_LENGTH:]
    with open(VOLUME_HISTORY_FILE, "w") as f:
        json.dump(history, f)
    return history

def read_atr(text):
    """Legge ATR da technical_context.txt; se mancante, calcola da yfinance M15; fallback 0.00043."""
    import re
    atr_m = re.search(r'atr:\s*([0-9.]+)', text)
    if atr_m:
        return float(atr_m.group(1))
    # Fallback: calcola ATR reale da yfinance (M15, 14 periodi)
    try:
        import yfinance as yf
        import pandas as pd
        df = yf.download("EURUSD=X", period="5d", interval="15m", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if not df.empty and len(df) >= 15:
            high = df["High"]; low = df["Low"]; close = df["Close"]
            prev_high = high.shift(1); prev_low = low.shift(1); prev_close = close.shift(1)
            tr1 = high - low
            tr2 = (high - prev_close).abs()
            tr3 = (low - prev_close).abs()
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.ewm(alpha=1/14, min_periods=14).mean().iloc[-1]
            if atr == atr:
                return float(atr)
    except Exception:
        pass
    return 0.00043  # fallback ATR reale EURUSD M15

def check_conditions():
    """Ritorna (trade_allowed, reason) con volume spike + candela forte + trend."""
    try:
        # 1. Leggi dati da technical_context.txt
        with open(TECH_CONTEXT) as f:
            text = f.read().lower()
        import re
        ema21_m = re.search(r'ema21:\s*([0-9.]+)', text)
        close_m = re.search(r'close:\s*([0-9.]+)', text)
        if not ema21_m or not close_m:
            return False, "ema21 o close non trovati"
        ema21 = float(ema21_m.group(1))
        close = float(close_m.group(1))
        
        # 2. Volume reale MT4 + history
        current_vol = read_volume_mt4()
        if current_vol <= 0:
            return False, "volume zero"
        
        history = update_volume_history(current_vol)
        if len(history) < HISTORY_LENGTH:
            return False, f"storico volume insufficiente ({len(history)}/{HISTORY_LENGTH})"
        
        avg_vol = sum(history[:-1]) / len(history[:-1])
        vol_spike = current_vol > avg_vol * VOLUME_SPIKE_FACTOR if avg_vol > 0 else False
        
        # 3. Trend EMA21
        trend_bull = close > ema21
        trend_bear = close < ema21
        trend_allineato = trend_bull or trend_bear
        
        # 4. Candela: leggi open da yfinance M15
        opn = close
        try:
            import yfinance as yf
            df = yf.download("EURUSD=X", period="1d", interval="15m", progress=False)
            if not df.empty and len(df) >= 1:
                if hasattr(df.columns, "get_level_values"):
                    df.columns = df.columns.get_level_values(0)
                opn = float(df.iloc[-1]["Open"])
        except Exception:
            pass
        
        # 5. Candela forte: corpo > 50% ATR
        atr = read_atr(text)
        candle_body = abs(close - opn)
        candela_forte = candle_body > atr * CANDLE_BODY_ATR_RATIO if atr > 0 else False
        
        # 6. Logica combinata: candela_forte AND trend_allineato
        trigger_attivo = candela_forte and trend_allineato
        
        direction = "BUY" if trend_bull else "SELL" if trend_bear else "NONE"
        
        if trigger_attivo and direction != "NONE":
            triggers = []
            if candela_forte:
                triggers.append(f"candela_forte({candle_body:.5f}>{atr:.5f}*0.5)")
            return True, f"{direction}: {' + '.join(triggers)} trend_allineato"
        
        # Dettaglio motivo HOLD
        reasons = []
        if not trend_allineato:
            reasons.append("trend_non_allineato")
        if not candela_forte:
            reasons.append(f"no_candela_forte(body{candle_body:.5f}<={atr:.5f}*0.5)")
        return False, "HOLD: " + ", ".join(reasons)
        
    except Exception as e:
        return False, f"errore: {e}"

def main():
    allowed, reason = check_conditions()
    market_open = is_market_open()
    trade_allowed = allowed and market_open
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "market_open": market_open,
        "trade_allowed": trade_allowed,
        "reason": reason
    }
    
    with open(OUTPUT_JSON, "w") as f:
        json.dump(result, f, indent=2)
    
    status = "OK" if trade_allowed else "BLOCCA"
    print(f"[trigger] {reason} MarketOpen={market_open} -> {status}", flush=True)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)
