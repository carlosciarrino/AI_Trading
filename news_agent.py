#!/usr/bin/env python3
"""news_agent.py v2 - Legge Investing.com RSS, filtra macro, sentiment.
Scrive news_context.txt (formato letto da orchestrator.py).
Loop ogni 10 minuti.
"""
import os, time, requests, re
from bs4 import BeautifulSoup

CONTEXT_PATH = os.path.expanduser("~/AI_Trading/news_context.txt")
RSS_URL = "https://it.investing.com/rss/news.rss"
MAX_TITLES = 15

# Keyword macro: se il titolo le contiene, e' macro-rilevante
MACRO_KEYWORDS = [
    # IT
    "fed", "bce", "tassi", "inflazione", "pil", "disoccupazione",
    "lavoro", "occupazione", "crescita", "recessione", "debito",
    "euro", "dollaro", "usd", "eur", "guerra", "dazi", "sanzioni",
    "petrolio", "oro", "wall street", "borsa", "mercati",
    "trimestrale", "utili", "occupazione", "stime",
    # EN (per RSS in inglese)
    "fed", "ecb", "rates", "inflation", "gdp", "unemployment",
    "jobs", "growth", "recession", "debt", "euro", "dollar",
    "war", "tariffs", "sanctions", "oil", "gold", "stocks",
    "earnings", "market", "economy",
]

# Parole positive / negative (EN + IT)
POSITIVE_WORDS = [
    "surge", "rally", "gain", "strong", "boost", "optimism", "deal",
    "peace", "growth", "record", "rialzo", "crescita", "forte",
    "accordo", "pace", "ottimismo", "positivo", "recupero", "balzo",
]
NEGATIVE_WORDS = [
    "crash", "plunge", "fear", "crisis", "war", "inflation",
    "recession", "block", "standoff", "dilemma", "cut",
    "crollo", "paura", "crisi", "guerra", "inflazione",
    "recessione", "blocco", "taglio", "perdita", "negativo",
    "calo", "ribasso", "tensione", "conflitto",
]


def fetch_titles():
    """Scarica RSS Investing.com, ritorna lista titoli."""
    try:
        r = requests.get(RSS_URL, timeout=10,
                         headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return []
        soup = BeautifulSoup(r.content, "xml")
        titles = []
        for item in soup.find_all("item"):
            t = item.title
            if t and t.text:
                titles.append(t.text.strip())
        return titles
    except Exception as e:
        print(f"Errore fetch_titles: {e}", flush=True)
        return []


def is_macro(title):
    """True se il titolo contiene keyword macro."""
    t = title.lower()
    return any(kw in t for kw in MACRO_KEYWORDS)


def sentiment_score(titles):
    """Calcola sentiment su lista titoli. Ritorna positivo|negativo|neutro."""
    text = " ".join(titles).lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in text)
    neg = sum(1 for w in NEGATIVE_WORDS if w in text)
    if pos > neg + 1:
        return "positivo"
    if neg > pos + 1:
        return "negativo"
    return "neutro"


def save_context():
    """Scarica, filtra, salva news_context.txt."""
    all_titles = fetch_titles()
    if not all_titles:
        # Nessun titolo: scrivi comunque il file per far vedere freschezza
        with open(CONTEXT_PATH, "w") as f:
            f.write(f"Ultime notizie macro (aggiornate {time.ctime()}):\n")
            f.write("(nessuna notizia disponibile)\n")
            f.write("Sentiment: neutro\n")
        print("news: nessun titolo", flush=True)
        return

    # Prima i macro, poi gli altri. Max MAX_TITLES.
    macro = [t for t in all_titles if is_macro(t)]
    non_macro = [t for t in all_titles if not is_macro(t)]
    selected = (macro + non_macro)[:MAX_TITLES]

    sent = sentiment_score(selected)
    with open(CONTEXT_PATH, "w") as f:
        f.write(f"Ultime notizie macro (aggiornate {time.ctime()}):\n")
        for t in selected:
            f.write(f"- {t}\n")
        f.write(f"Sentiment: {sent}\n")
    print(f"news: {len(selected)} titoli ({len(macro)} macro), sentiment={sent}",
          flush=True)


if __name__ == "__main__":
    while True:
        try:
            save_context()
        except Exception as e:
            print(f"Errore news_agent: {e}", flush=True)
        time.sleep(600)  # 10 minuti
