import requests, time, os, json, re
from bs4 import BeautifulSoup

CONTEXT_PATH = os.path.expanduser("~/AI_Trading/social_context.txt")

def get_trending_social():
    try:
        # Google Trends/News (gratis) per il sentiment generale
        url = "https://news.google.com/rss/search?q=forex+OR+trump+OR+tiktok&hl=en-US&gl=US&ceid=US:en"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, "xml")
        titles = [item.title.text for item in soup.find_all("item")[:10]]
        return titles
    except:
        return []

POSITIVE_WORDS = ["surge", "rally", "gain", "strong", "boost", "optimism",
                  "deal", "peace", "growth", "record"]
NEGATIVE_WORDS = ["crash", "plunge", "fear", "crisis", "war", "inflation",
                  "recession", "block", "standoff", "dilemma", "cut"]

def sentiment_score(titles):
    text = " ".join(titles).lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in text)
    neg = sum(1 for w in NEGATIVE_WORDS if w in text)
    if pos > neg:
        return "positivo"
    if neg > pos:
        return "negativo"
    return "neutro"

def save_context():
    titles = get_trending_social()
    sent = sentiment_score(titles)
    with open(CONTEXT_PATH, "w") as f:
        f.write(f"Sentiment social (aggiornato {time.ctime()}):\n")
        for t in titles:
            f.write(f"- {t}\n")
        f.write(f"Sentiment: {sent}\n")
    print(f"Sentiment social aggiornato: {sent}")

while True:
    save_context()
    time.sleep(600)  # aggiorna ogni 10 minuti
