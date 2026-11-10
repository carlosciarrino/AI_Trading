#!/usr/bin/env python3
"""trigger_engine.py - Gate di mercato allineato a get_ema_volume_signal.
Controlla: Volume yfinance 1.5x + Trend EMA21 + Candela close vs open.
Scrive triggers.json per l'orchestratore.
"""
import json, os, time
from datetime import datetime, timezone

BASE = "/home/carlo/AI_Trading"
TECH_CONTEXT = os.path.join(BASE, "technical_context.txt")
OUTPUT_JSON = os.path.join(BASE, "triggers.json")

VOLUME_SPIKE_FACTOR = 1.5

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

def check_conditions():
    """Ritorna (trade_allowed, reason) replicando logica get_ema_volume_signal."""
    try:
        # 1. Leggi EMA21 da technical_context.txt
        with open(TECH_CONTEXT) as f:
            text = f.read().lower()
        import re
        ema21_m = re.search(r'ema21:\s*([0-9.]+)', text)
        if not ema21_m:
            return False, "ema21 non trovata"
        ema21 = float(ema21_m.group(1))
        
        # 2. Scarica ultime candele M15 da yfinance
        import yfinance as yf
        df = yf.download("EURUSD=X", period="1d", interval="15m", progress=False)
        if df.empty or len(df) < 21:
            return False, "dati insufficienti"
        if hasattr(df.columns, "get_level_values"):
            df.columns = df.columns.get_level_values(0)
        
        last = df.iloc[-1]
        close = float(last["Close"])
        opn = float(last["Open"])
        vol = float(last["Volume"])
        vol_ma = float(df["Volume"].iloc[-21:-1].mean())
        
        # 3. Condizioni identiche a get_ema_volume_signal
        trend_bull = close > ema21
        trend_bear = close < ema21
        vol_spike = vol > vol_ma * VOLUME_SPIKE_FACTOR if vol_ma > 0 else False
        candle_bull = close > opn
        candle_bear = close < opn
        
        buy_cond = trend_bull and vol_spike and candle_bull
        sell_cond = trend_bear and vol_spike and candle_bear
        
        if buy_cond:
            return True, f"BUY: close{close:.5f}>ema21{ema21:.5f} vol{vol:.0f}>{vol_ma:.0f}*1.5 candle_bull"
        if sell_cond:
            return True, f"SELL: close{close:.5f}<ema21{ema21:.5f} vol{vol:.0f}>{vol_ma:.0f}*1.5 candle_bear"
        
        # Dettaglio motivo HOLD
        reasons = []
        if not trend_bull and not trend_bear:
            reasons.append("close==ema21")
        if not vol_spike:
            reasons.append(f"vol{vol:.0f}<={vol_ma:.0f}*1.5")
        if not candle_bull and not candle_bear:
            reasons.append("doji")
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
