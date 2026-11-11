#!/usr/bin/env python3
"""social_scout.py - Cerca sentiment EURUSD su Reddit via Agent-Reach.
Scrive social_context.txt per l'orchestratore.
"""
import json, os, subprocess, sys
from datetime import datetime

BASE = "/home/carlo/Progetti/AI_Trading"
OUTPUT_FILE = os.path.join(BASE, "social_context.txt")
AGENT_REACH_VENV = "/home/carlo/AI_Trading_sandbox/agent_reach_test/venv_reach/bin/python"
AGENT_REACH_CMD = "/home/carlo/AI_Trading_sandbox/agent_reach_test/venv_reach/bin/agent-reach"

POSITIVE_KEYWORDS = ['buy', 'bullish', 'uptrend', 'long', 'support', 'bounce', 'recovery', 'rally', 'gain', 'profit', 'strong', 'bull']
NEGATIVE_KEYWORDS = ['sell', 'bearish', 'downtrend', 'short', 'resistance', 'drop', 'crash', 'fall', 'loss', 'weak', 'bear', 'dump']

def calculate_sentiment(text):
    """Calcola sentiment semplice basato su keyword."""
    text_lower = text.lower()
    pos_count = sum(1 for kw in POSITIVE_KEYWORDS if kw in text_lower)
    neg_count = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text_lower)
    
    if pos_count > neg_count:
        return "positivo"
    elif neg_count > pos_count:
        return "negativo"
    return "neutro"

def search_reddit():
    """Esegue agent-reach reddit search EURUSD."""
    try:
        result = subprocess.run(
            [AGENT_REACH_CMD, "reddit", "search", "EURUSD", "--limit", "10"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return None, f"Errore agent-reach: {result.stderr}"
        return json.loads(result.stdout), None
    except subprocess.TimeoutExpired:
        return None, "Timeout agent-reach"
    except json.JSONDecodeError as e:
        return None, f"JSON decode error: {e}"
    except Exception as e:
        return None, f"Errore: {e}"

def main():
    data, error = search_reddit()
    
    if error or not data or not data.get("ok"):
        sentiment = "neutro"
        posts_text = f"Errore ricerca: {error or 'dati non validi'}"
    else:
        items = data.get("items", [])
        if not items:
            sentiment = "neutro"
            posts_text = "Nessun post trovato"
        else:
            sentiments = []
            posts_summary = []
            for item in items[:10]:
                title = item.get("title", "")
                text = item.get("text", "")
                combined = f"{title} {text}"
                s = calculate_sentiment(combined)
                sentiments.append(s)
                posts_summary.append(f"{title[:80]}")
            
            pos = sentiments.count("positivo")
            neg = sentiments.count("negativo")
            neu = sentiments.count("neutro")
            
            if pos > neg and pos > neu:
                sentiment = "positivo"
            elif neg > pos and neg > neu:
                sentiment = "negativo"
            else:
                sentiment = "neutro"
            
            posts_text = " | ".join(posts_summary[:3])
    
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"Sentiment: {sentiment}\n")
        f.write(f"Post: {posts_text}\n")
        f.write(f"Updated: {datetime.now().isoformat()}\n")
    
    print(f"[social_scout] Sentiment: {sentiment} | Posts: {posts_text[:100]}", flush=True)

if __name__ == "__main__":
    main()
