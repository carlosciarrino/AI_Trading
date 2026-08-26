import feedparser, time, json, os

NEWS_FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "http://feeds.reuters.com/reuters/businessNews",
    "https://feeds.bbci.co.uk/news/business/rss.xml"
]
KEYWORDS = ["war", "crisis", "election", "inflation", "rate", "oil", "sanctions", "conflict"]
CONTEXT_PATH = os.path.expanduser("~/AI_Trading/news_context.txt")

def fetch_news():
    headlines = []
    for feed_url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:
                title = entry.title.lower()
                if any(k in title for k in KEYWORDS):
                    headlines.append(entry.title)
        except:
            pass
    
    with open(CONTEXT_PATH, "w") as f:
        f.write(f"Ultime notizie macro importanti (aggiornate {time.ctime()}):\n")
        for h in headlines:
            f.write(f"- {h}\n")
    print("Notizie geopolitiche aggiornate.")

while True:
    fetch_news()
    time.sleep(1800)  # aggiorna ogni 30 minuti
