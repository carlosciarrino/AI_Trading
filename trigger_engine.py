#!/usr/bin/env python3
"""trigger_engine.py - Calcola 3 trigger di mercato: Volume, Regime, News.
Scrive triggers.json per l'orchestratore.
"""
import json, os, time
from datetime import datetime

BASE = "/home/carlo/AI_Trading"
VOLUME_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/volume_data.json"
TECH_CONTEXT = os.path.join(BASE, "technical_context.txt")
NEWS_CONTEXT = os.path.join(BASE, "news_context.txt")
OUTPUT_JSON = os.path.join(BASE, "triggers.json")
FORECAST_JSON = os.path.join(BASE, "forecast.json")

# Soglie
VOLUME_SPIKE_FACTOR = 1.5  # Volume > 2x media
ADX_TREND_THRESHOLD = 25.0  # ADX > 25 = trend forte

def check_volume_trigger():
    """Ritorna True se c'e' uno spike di volume (da yfinance M15)."""
    try:
        import yfinance as yf
        df = yf.download("EURUSD=X", period="1d", interval="15m", progress=False)
        if df.empty or len(df) < 10:
            return False, "dati insufficienti"
        
        if hasattr(df.columns, "get_level_values"):
            df.columns = df.columns.get_level_values(0)
        
        vol = df["Volume"].values
        current_vol = vol[-1]
        avg_vol = vol[-11:-1].mean()
        
        if avg_vol > 0 and current_vol > avg_vol * VOLUME_SPIKE_FACTOR:
            return True, f"spike {current_vol/avg_vol:.1f}x"
    except Exception:
        pass
    return False, "neutro"

def check_regime_trigger():
    """Ritorna True se il mercato e' in trend forte o volatile."""
    try:
        with open(TECH_CONTEXT) as f:
            text = f.read().lower()
        # Controlla ADX
        import re
        match = re.search(r'adx:\s*([0-9.]+)', text)
        if match:
            adx = float(match.group(1))
            if adx > ADX_TREND_THRESHOLD:
                return True, f"ADX {adx:.1f} (trend forte)"
        # Controlla se c'e' un trend definito
        if 'bull=true' in text or 'bear=true' in text:
            return True, "trend definito"
    except Exception:
        pass
    return False, "calmo/neutro"

def check_news_trigger():
    """Ritorna True se c'e' una notizia ad alto impatto."""
    try:
        with open(NEWS_CONTEXT) as f:
            text = f.read().lower()
        # Keyword ad alto impatto
        high_impact = ['fed', 'bce', 'war', 'crash', 'inflation', 'tassi', 'guerra']
        if any(k in text for k in high_impact):
            # Controlla se il sentiment e' estremo
            if 'sentiment: positivo' in text or 'sentiment: negativo' in text:
                return True, "notizia macro + sentiment"
    except Exception:
        pass
    return False, "neutro"

def check_forecast_trigger():
    """Ritorna True se TimesFM prevede un movimento direzionale."""
    try:
        with open(FORECAST_JSON) as f:
            data = json.load(f)
        direction = data.get("direction", "NEUTRAL")
        if direction in ("BULLISH", "BEARISH"):
            return True, direction
    except Exception:
        pass
    return False, "neutro"

def is_market_open():
    """Controlla se il mercato forex e' aperto (Londra/NY)."""
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    if now.weekday() == 4 and now.hour >= 22:
        return False
    if now.weekday() == 5:
        return False
    if now.weekday() == 6 and now.hour < 22:
        return False
    return True

def main():
    t_vol, msg_vol = check_volume_trigger()
    t_reg, msg_reg = check_regime_trigger()
    t_news, msg_news = check_news_trigger()
    t_for, msg_for = check_forecast_trigger()
    
    # Punteggio ponderato
    score = 0.0
    if t_vol: score += 2.0
    if t_reg: score += 1.5
    if t_news: score += 1.0
    if t_for: score += 1.5
    
    active_count = score
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "volume": {"active": t_vol, "reason": msg_vol},
        "regime": {"active": t_reg, "reason": msg_reg},
        "news": {"active": t_news, "reason": msg_news},
        "forecast": {"active": t_for, "reason": msg_for},
        "active_count": active_count,
        "market_open": is_market_open(),
        "trade_allowed": (active_count >= 2.0) and is_market_open()  # Almeno 2 trigger su 3
    }
    
    with open(OUTPUT_JSON, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"[trigger] Vol={t_vol}(2.0) Reg={t_reg}(1.5) News={t_news}(1.0) For={t_for}(1.5) -> Score={score:.1f} -> {'OK' if result['trade_allowed'] else 'BLOCCA'}", flush=True)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)  # Ogni minuto
