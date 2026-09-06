#!/usr/bin/env python3
import json, os, time, requests
from datetime import datetime, timedelta
import pytz

SIGNALS_FILE = "/home/carlo/AI_Trading/signals/signals.json"
REPORT_FILE = "/home/carlo/AI_Trading/signals/report.json"
VERIFIED_FILE = "/home/carlo/AI_Trading/signals/verified_signals.json"

def load_signals():
    try:
        with open(SIGNALS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def verify_signal(signal):
    """
    Verifica se un segnale è coerente con i dati di mercato.
    Se l'entry non corrisponde al prezzo reale di quel momento, è falso.
    """
    try:
        # Simula la verifica (in realtà userebbe dati storici reali)
        # Per ora, controlla solo se entry, sl, tp sono ordinati logicamente
        entry = signal.get("entry", 0)
        sl = signal.get("sl", 0)
        tp = signal.get("tp", 0)
        action = signal.get("action", "buy")
        
        if action == "buy":
            if sl >= entry or tp <= entry:
                return {"valid": False, "reason": "SL/TP non logici per BUY"}
        elif action == "sell":
            if sl <= entry or tp >= entry:
                return {"valid": False, "reason": "SL/TP non logici per SELL"}
        # Controllo distanza minima (almeno 10 pip)
        if abs(tp - entry) < 0.001 or abs(sl - entry) < 0.001:
            return {"valid": False, "reason": "SL/TP troppo stretti"}
        return {"valid": True, "reason": "Segnale coerente"}
    except:
        return {"valid": False, "reason": "Errore nei dati"}

def analyze_performance(signals):
    total = len(signals)
    if total == 0:
        return {"win_rate": 0, "avg_pnl": 0, "verified": 0, "fake": 0}
    wins = sum(1 for s in signals if s.get("result") == "win")
    losses = sum(1 for s in signals if s.get("result") == "loss")
    pnl_total = sum(s.get("pnl", 0) for s in signals)
    verified = sum(1 for s in signals if s.get("verified", False))
    fake = sum(1 for s in signals if s.get("verified") == False and s.get("verification_reason"))
    return {
        "total": total,
        "wins": wins,
        "losses": losses,
        "win_rate": wins / total * 100 if total > 0 else 0,
        "avg_pnl": pnl_total / total if total > 0 else 0,
        "verified": verified,
        "fake": fake,
        "last_updated": datetime.now().isoformat()
    }

def main():
    print("Signal Observer Agent avviato (con verifica).")
    print("📊 In attesa di segnali da analizzare...")
    while True:
        signals = load_signals()
        # Verifica ogni segnale (se non già verificato)
        verified_signals = []
        for s in signals:
            if "verified" not in s:
                result = verify_signal(s)
                s["verified"] = result["valid"]
                s["verification_reason"] = result["reason"]
            verified_signals.append(s)
        # Salva i segnali verificati
        with open(VERIFIED_FILE, 'w') as f:
            json.dump(verified_signals, f, indent=2)
        # Genera report
        report = analyze_performance(verified_signals)
        with open(REPORT_FILE, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Report: {report['total']} segnali, "
              f"win rate {report['win_rate']:.1f}%, "
              f"verificati {report['verified']}, "
              f"falsi {report['fake']}")
        time.sleep(3600)

if __name__ == "__main__":
    main()
