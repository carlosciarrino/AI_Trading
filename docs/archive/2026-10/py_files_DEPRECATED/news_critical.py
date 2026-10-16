import feedparser
import time
import os

# Fonti: BBC World, Reuters
FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "http://feeds.reuters.com/reuters/businessNews"
]
KEYWORDS = ["war", "crisis", "election", "inflation", "rate", "oil", "sanctions", "conflict", "geopolitical"]
OUTPUT = os.path.expanduser("~/AI_Trading/news_critical_context.txt")

def fetch_critical_news():
    headlines = []
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                title = entry.title.lower()
                if any(k in title for k in KEYWORDS):
                    headlines.append(entry.title)
        except:
            pass
    with open(OUTPUT, "w") as f:
        f.write(f"Notizie critiche geopolitiche aggiornate {time.ctime()}:\n")
        for h in headlines:
            f.write(f"- {h}\n")
    print("News Critical aggiornate.")

while True:
    fetch_critical_news()
    time.sleep(1800)  # Ogni 30 minuti
