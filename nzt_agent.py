#!/usr/bin/env python3
import json, os, time
from datetime import datetime, timedelta
import pytz

CONFIG_PATH = os.path.expanduser("~/AI_Trading/config.json")
SCORE_FILE = "/tmp/nzt_score.txt"

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def get_frankfurt_range():
    tz = pytz.timezone("Europe/Berlin")
    now = datetime.now(tz)
    if now.weekday() >= 5:
        return None
    open_time = now.replace(hour=8, minute=0, second=0, microsecond=0)
    close_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
    if now < open_time or now > close_time:
        return None
    try:
        with open(os.path.expanduser("~/mt4_shared/orders.json")) as f:
            orders = json.load(f)
        prices = [o.get("price", 0) for o in orders if o.get("price")]
        if not prices:
            return None
        return {"high": max(prices), "low": min(prices)}
    except:
        return None

def main():
    config = load_config()
    while True:
        try:
            range_data = get_frankfurt_range()
            if range_data is None:
                score = 0.0
            else:
                with open(os.path.expanduser("~/mt4_shared/orders.json")) as f:
                    orders = json.load(f)
                if orders:
                    last_price = orders[-1].get("price", 1.0)
                    high = range_data["high"]
                    low = range_data["low"]
                    if last_price > high:
                        score = 1.0
                    elif last_price < low:
                        score = -1.0
                    else:
                        score = 0.0
                else:
                    score = 0.0
            with open(SCORE_FILE, "w") as f:
                f.write(f"{score:.4f}")
        except Exception as e:
            print(f"Errore NZT: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
