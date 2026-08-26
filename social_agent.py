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

def save_context():
    titles = get_trending_social()
    with open(CONTEXT_PATH, "w") as f:
        f.write(f"Sentiment social (aggiornato {time.ctime()}):\n")
        for t in titles:
            f.write(f"- {t}\n")
    print("Sentiment social aggiornato.")

while True:
    save_context()
    time.sleep(600)  # aggiorna ogni 10 minuti
