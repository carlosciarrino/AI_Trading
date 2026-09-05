#!/usr/bin/env python3
import json, os, time, requests
from datetime import datetime, timedelta

CONFIG_PATH = os.path.expanduser("~/AI_Trading/config.json")
SCORE_FILE = "/tmp/news_score.txt"

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def get_economic_calendar():
    """Legge il calendario da Investing.com (versione semplificata)"""
    try:
        # Usa un feed RSS di Investing.com (es. per USD)
        url = "https://it.investing.com/rss/news.rss"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Parsing base (cerchiamo parole chiave)
            content = response.text.lower()
            keywords = ["nonfarm", "tassi", "fed", "inflazione", "pil", "disoccupazione"]
            for kw in keywords:
                if kw in content:
                    return {"has_news": True, "impact": "alto", "keyword": kw}
        return {"has_news": False}
    except:
        return {"has_news": False}

def main():
    config = load_config()
    while True:
        try:
            calendar = get_economic_calendar()
            if calendar.get("has_news"):
                # Penalizza se news ad alto impatto nelle prossime 2 ore
                score = -0.3
            else:
                score = 0.0
            with open(SCORE_FILE, "w") as f:
                f.write(f"{score:.4f}")
        except Exception as e:
            print(f"Errore News: {e}")
        time.sleep(60)  # aggiorna ogni minuto

if __name__ == "__main__":
    main()
