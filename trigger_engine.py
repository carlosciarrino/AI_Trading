#!/usr/bin/env python3
"""trigger_engine.py - Calcola trigger di mercato: Volume e Trend (EMA21).
Scrive triggers.json per l'orchestratore.
"""
import json, os, time
from datetime import datetime

BASE = "/home/carlo/AI_Trading"
VOLUME_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/volume_data.json"
TECH_CONTEXT = os.path.join(BASE, "technical_context.txt")
OUTPUT_JSON = os.path.join(BASE, "triggers.json")

VOLUME_SPIKE_FACTOR = 1.5
VOLUME_HISTORY_FILE = os.path.join(BASE, "volume_history.json")

def check_volume_trigger():
    """Ritorna True se c'e' uno spike di volume > 1.5x media."""
    try:
        with open(VOLUME_JSON) as f:
            data = json.load(f)
        current_vol = data.get("volume", 0)
        if current_vol <= 0:
            return False, "volume zero"
        
        history = []
        if os.path.exists(VOLUME_HISTORY_FILE):
            try:
                with open(VOLUME_HISTORY_FILE) as f:
                    history = json.load(f)
            except Exception:
                history = []
        
        history.append(current_vol)
        history = history[-20:]
        with open(VOLUME_HISTORY_FILE, "w") as f:
            json.dump(history, f)
        
        if len(history) < 5:
            return False, "storico insufficiente"
        
        avg_vol = sum(history[:-1]) / len(history[:-1])
        if avg_vol > 0 and current_vol > avg_vol * VOLUME_SPIKE_FACTOR:
            return True, f"spike {current_vol/avg_vol:.1f}x"
    except Exception:
        pass
    return False, "neutro"

def check_trend_aligned():
    """Ritorna True se il trend e' allineato (EMA21 direction)."""
    try:
        with open(TECH_CONTEXT) as f:
            text = f.read().lower()
        
        # Formato reale: "Trend: bull=False bear=True" o "bull=True" / "bear=True"
        if 'bull=true' in text:
            return True, "trend bull allineato"
        if 'bear=true' in text:
            return True, "trend bear allineato"
        
        # Fallback: ADX > 25 con trend definito
        if 'adx:' in text:
            import re
            match = re.search(r'adx:\s*([0-9.]+)', text)
            if match and float(match.group(1)) > 25:
                if 'bull=true' in text or 'bear=true' in text:
                    return True, "trend forte"
    except Exception:
        pass
    return False, "trend non allineato"

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
    t_trend, msg_trend = check_trend_aligned()
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "volume": {"active": t_vol, "reason": msg_vol},
        "trend": {"active": t_trend, "reason": msg_trend},
        "market_open": is_market_open(),
        "trade_allowed": t_vol and t_trend and is_market_open()
    }
    
    with open(OUTPUT_JSON, "w") as f:
        json.dump(result, f, indent=2)
    
    status = "OK" if result["trade_allowed"] else "BLOCCA"
    print(f"[trigger] Vol={t_vol} Trend={t_trend} MarketOpen={result['market_open']} -> {status}", flush=True)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)
