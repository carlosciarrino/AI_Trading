import requests, logging, feedparser
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_forex_live_news(limit=3):
    try:
        feed = feedparser.parse("https://www.forexlive.com/feed/news")
        news = []
        for entry in feed.entries[:limit]:
            news.append({'title': entry.title, 'summary': entry.summary[:200]})
        return news
    except Exception as e:
        logger.error(f"ForexLive: {e}")
        return []

def analyze_sentiment(news_items):
    if not news_items:
        return "Nessuna notizia"
    text = "\n".join([f"- {n['title']}" for n in news_items])
    try:
        resp = requests.post("http://localhost:11434/api/generate",
                             json={"model": "llama3.2:3b", "prompt": f"Sentiment di queste notizie (POSITIVO/NEUTRO/NEGATIVO):\n{text}", "stream": False},
                             timeout=30)
        return resp.json().get("response", "Sentiment non disponibile")
    except:
        return "Sentiment non disponibile"
