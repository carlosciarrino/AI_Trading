import snscrape.modules.twitter as sntwitter
import pandas as pd, requests, logging
from datetime import datetime, timedelta

def get_tweets(query="EURUSD OR forex", limit=10):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{query} since:{datetime.now().strftime('%Y-%m-%d')}").get_items()):
        if i >= limit:
            break
        tweets.append({
            'date': tweet.date,
            'content': tweet.content[:200],
            'user': tweet.user.username
        })
    return tweets

def analyze_sentiment(tweets, model="llama3.2:3b"):
    if not tweets:
        return "Nessun tweet recente."
    text = "\n".join([f"- {t['content']}" for t in tweets[:5]])
    prompt = f"Analizza il sentiment di questi tweet sul forex. Dai un giudizio: POSITIVO, NEUTRO, NEGATIVO.\nTweet:\n{text}\nSentiment:"
    try:
        resp = requests.post("http://localhost:11434/api/generate", json={"model": model, "prompt": prompt, "stream": False}, timeout=30)
        return resp.json().get("response", "Sentiment non disponibile")
    except:
        return "Errore sentiment"

if __name__ == "__main__":
    tweets = get_tweets(limit=5)
    print("📱 Tweet:", tweets)
    print("📊 Sentiment:", analyze_sentiment(tweets))
