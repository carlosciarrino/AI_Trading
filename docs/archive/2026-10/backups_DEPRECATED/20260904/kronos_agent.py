#!/usr/bin/env python3
import json, os, time, sys
import requests

SCORE_FILE = "/tmp/kronos_score.txt"
CONFIG_PATH = os.path.expanduser("~/AI_Trading/config.json")

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def get_latest_ohlcv():
    try:
        with open(os.path.expanduser("~/mt4_shared/orders.json")) as f:
            orders = json.load(f)
        if orders:
            last = orders[-1]
            return {"open": last.get("price", 1.0), "close": last.get("price", 1.0)}
    except:
        pass
    return {"open": 1.0, "close": 1.0}

def main():
    config = load_config()
    print("✅ Kronos Agent avviato (versione leggera)")
    while True:
        try:
            data = get_latest_ohlcv()
            diff = data["close"] - data["open"]
            score = max(-1.0, min(1.0, diff * 200))
            with open(SCORE_FILE, "w") as f:
                f.write(f"{score:.4f}")
        except Exception as e:
            print(f"Errore Kronos: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
