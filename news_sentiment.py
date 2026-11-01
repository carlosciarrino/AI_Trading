#!/usr/bin/env python3
"""news_sentiment.py - Calcola sentiment con FinBERT su news_context.txt."""
import os, json, re
from datetime import datetime

NEWS_CONTEXT = "/home/carlo/AI_Trading/news_context.txt"
OUTPUT_JSON = "/home/carlo/AI_Trading/news_sentiment.json"

def extract_titles(text):
    """Estrae i titoli dal formato 'Ultime notizie macro...'"""
    titles = []
    for line in text.split('\n'):
        line = line.strip()
        if line and not line.startswith('Ultime notizie') and not line.startswith('Sentiment:'):
            # Rimuove numerazione o bullet
            line = re.sub(r'^[-•\d.]+\s*', '', line)
            if len(line) > 10:
                titles.append(line)
    return titles[:10]  # Max 10 titoli

def main():
    try:
        with open(NEWS_CONTEXT) as f:
            text = f.read()
    except Exception:
        print("[news_sentiment] news_context.txt non trovato.", flush=True)
        return

    titles = extract_titles(text)
    if not titles:
        print("[news_sentiment] Nessun titolo estratto.", flush=True)
        return

    # 1. Leggi il sentiment keyword dal file originale
    keyword_sent = "neutro"
    for line in text.lower().split('\n'):
        if 'sentiment:' in line:
            if 'positivo' in line:
                keyword_sent = "positivo"
            elif 'negativo' in line:
                keyword_sent = "negativo"
            break

    # 2. Se le keyword sono forti, usa quelle (FinBERT non serve)
    if keyword_sent in ("positivo", "negativo"):
        result = {
            "timestamp": datetime.now().isoformat(),
            "sentiment": keyword_sent,
            "source": "keyword",
            "avg_score": 0.0,
            "n_titles": len(titles)
        }
        with open(OUTPUT_JSON, "w") as f:
            json.dump(result, f, indent=2)
        print(f"[news_sentiment] {keyword_sent} (keyword, {len(titles)} titoli)", flush=True)
        return

    # 3. Altrimenti, usa FinBERT
    from transformers import pipeline
    classifier = pipeline('sentiment-analysis', model='ProsusAI/finbert')

    scores = []
    for t in titles:
        try:
            res = classifier(t[:512])[0]
            if res['label'] == 'positive':
                scores.append(res['score'])
            elif res['label'] == 'negative':
                scores.append(-res['score'])
            else:
                scores.append(0.0)
        except Exception:
            scores.append(0.0)

    avg_score = sum(scores) / len(scores) if scores else 0.0
    
    if avg_score > 0.15:
        sentiment = "positivo"
    elif avg_score < -0.15:
        sentiment = "negativo"
    else:
        sentiment = "neutro"

    result = {
        "timestamp": datetime.now().isoformat(),
        "sentiment": sentiment,
        "source": "finbert",
        "avg_score": round(avg_score, 4),
        "n_titles": len(titles),
        "scores": [round(s, 3) for s in scores]
    }

    with open(OUTPUT_JSON, "w") as f:
        json.dump(result, f, indent=2)

    print(f"[news_sentiment] {sentiment} (score {avg_score:.2f}, {len(titles)} titoli)", flush=True)

if __name__ == "__main__":
    main()
