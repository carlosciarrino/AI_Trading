#!/usr/bin/env python3
"""trigger_engine.py - Gate di mercato con volume MT4 reale.
Controlla: Volume MT4 1.5x media + Trend EMA21 + Candela close vs open.
Scrive triggers.json per l'orchestratore.
"""
import json, os, time
from datetime import datetime, timezone

BASE = "/home/carlo/AI_Trading"
TECH_CONTEXT = os.path.join(BASE, "technical_context.txt")
VOLUME_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/volume_data.json"
VOLUME_HISTORY_FILE = os.path.join(BASE, "volume_history.json")
OUTPUT_JSON = os.path.join(BASE, "triggers.json")

VOLUME_SPIKE_FACTOR = 1.5
HISTORY_LENGTH = 5

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

def check_conditions():
    """Ritorna (trade_allowed, reason) con volume MT4 + EMA21 + candela."""
    try:
        # 1. Leggi EMA21 e Close da technical_context.txt
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
        
        # Media degli ultimi 4 (escluso il corrente)
        avg_vol = sum(history[:-1]) / len(history[:-1])
        vol_spike = current_vol > avg_vol * VOLUME_SPIKE_FACTOR if avg_vol > 0 else False
        
        # 3. Trend EMA21
        trend_bull = close > ema21
        trend_bear = close < ema21
        
        # 4. Candela: approssima open ~= close (tick data) oppure leggi open da yfinance
        # Usiamo yfinance solo per open della candela M15
        opn = close
        try:
            import yfinance as yf
            df = yf.download("EURUSD=X", period="1d", interval="15m", progress=False)
            if not df.empty and len(df) >= 1:
                if hasattr(df.columns, "get_level_values"):
                    df.columns = df.columns.get_level_values(0)
                opn = float(df.iloc[-1]["Open"])
        except Exception:
            pass  # fallback open = close
        
        candle_bull = close > opn
        candle_bear = close < opn
        
        buy_cond = trend_bull and vol_spike and candle_bull
        sell_cond = trend_bear and vol_spike and candle_bear
        
        if buy_cond:
            return True, f"BUY: close{close:.5f}>ema21{ema21:.5f} vol{current_vol}>{avg_vol:.0f}*1.5 candle_bull"
        if sell_cond:
            return True, f"SELL: close{close:.5f}<ema21{ema21:.5f} vol{current_vol}>{avg_vol:.0f}*1.5 candle_bear"
        
        # Dettaglio motivo HOLD
        reasons = []
        if not trend_bull and not trend_bear:
            reasons.append("close==ema21")
        if not vol_spike:
            reasons.append(f"vol{current_vol}<={avg_vol:.0f}*1.5")
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
