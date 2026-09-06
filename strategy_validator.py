#!/usr/bin/env python3
import json, os, time, subprocess
from datetime import datetime

REPORT_FILE = "/home/carlo/AI_Trading/strategie_valide.json"
STRATEGY_LIST = "/home/carlo/AI_Trading/strategie_trovate.txt"

def load_strategies():
    """Legge le strategie trovate da skill_researcher/strategy_tester"""
    try:
        with open(STRATEGY_LIST, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def test_strategy(strategy):
    """Lancia il tester sulla strategia e restituisce un punteggio di qualità"""
    # Simula un test (in realtà chiama strategy_tester_agent)
    try:
        result = subprocess.run(
            ["python3", "/home/carlo/AI_Trading/strategy_tester_agent.py", "--test", strategy],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            # Parsing del report (semplificato)
            lines = result.stdout.split('\n')
            win_rate = 0.0
            drawdown = 0.0
            for line in lines:
                if "win rate" in line.lower():
                    win_rate = float(line.split(':')[1].strip().replace('%','')) / 100
                if "drawdown" in line.lower():
                    drawdown = float(line.split(':')[1].strip().replace('%','')) / 100
            return {"win_rate": win_rate, "drawdown": drawdown, "valid": win_rate > 0.5 and drawdown < 0.1}
        return {"valid": False}
    except:
        return {"valid": False}

def main():
    print("Strategy Validator avviato")
    while True:
        try:
            strategies = load_strategies()
            valid_strategies = []
            for s in strategies[:10]:  # Limita a 10 per non sovraccaricare
                result = test_strategy(s)
                if result.get("valid"):
                    valid_strategies.append({
                        "strategy": s,
                        "win_rate": result.get("win_rate", 0),
                        "drawdown": result.get("drawdown", 0),
                        "timestamp": datetime.now().isoformat()
                    })
            if valid_strategies:
                with open(REPORT_FILE, 'w') as f:
                    json.dump(valid_strategies, f, indent=2)
                print(f"✅ Trovate {len(valid_strategies)} strategie valide.")
        except Exception as e:
            print(f"Errore: {e}")
        time.sleep(3600)  # Ogni ora

if __name__ == "__main__":
    main()
