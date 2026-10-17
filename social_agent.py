import requests, time, os, json, re
from bs4 import BeautifulSoup
from datetime import datetime

CONTEXT_PATH = os.path.expanduser("~/AI_Trading/social_context.txt")
HISTORY_PATH = os.path.expanduser("~/AI_Trading/social_history.json")

POSITIVE_WORDS = ["surge", "rally", "gain", "strong", "boost", "optimism",
                  "deal", "peace", "growth", "record", "rialzo", "crescita",
                  "forte", "accordo", "pace", "ottimismo", "positivo"]
NEGATIVE_WORDS = ["crash", "plunge", "fear", "crisis", "war", "inflation",
                  "recession", "block", "standoff", "dilemma", "cut",
                  "crollo", "paura", "crisi", "guerra", "inflazione",
                  "recessione", "blocco", "taglio", "perdita", "negativo"]


def get_trending_social():
    try:
        url = "https://news.google.com/rss/search?q=forex+OR+trump+OR+tiktok&hl=en-US&gl=US&ceid=US:en"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, "xml")
        titles = [item.title.text for item in soup.find_all("item")[:10]]
        return titles
    except:
        return []


def sentiment_score(titles):
    text = " ".join(titles).lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in text)
    neg = sum(1 for w in NEGATIVE_WORDS if w in text)
    if pos > neg:
        return "positivo", pos, neg
    if neg > pos:
        return "negativo", pos, neg
    return "neutro", pos, neg


def intensity(pos, neg):
    """1-5: quanti match totali."""
    total = pos + neg
    if total == 0:
        return 1
    if total <= 2:
        return 2
    if total <= 4:
        return 3
    if total <= 6:
        return 4
    return 5


def load_history():
    try:
        with open(HISTORY_PATH) as f:
            return json.load(f)
    except:
        return []


def save_history(history):
    # tieni ultimi 30 giorni
    cutoff = time.time() - 30 * 86400
    history = [h for h in history if h.get("timestamp", 0) >= cutoff]
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


def compute_change(current_volume, history):
    """↑↓→ rispetto a media storica."""
    if not history:
        return "→"
    volumes = [h.get("volume", 0) for h in history]
    avg = sum(volumes) / len(volumes) if volumes else current_volume
    if current_volume > avg * 1.2:
        return "↑"
    if current_volume < avg * 0.8:
        return "↓"
    return "→"


def save_context():
    titles = get_trending_social()
    volume = len(titles)
    sent, pos, neg = sentiment_score(titles)
    inten = intensity(pos, neg)

    history = load_history()
    change = compute_change(volume, history)
    avg_30 = 0
    if history:
        volumes = [h.get("volume", 0) for h in history]
        avg_30 = round(sum(volumes) / len(volumes), 1)

    # Salva nello storico
    history.append({
        "timestamp": time.time(),
        "volume": volume,
        "sentiment": sent,
        "intensity": inten,
    })
    save_history(history)

    with open(CONTEXT_PATH, "w") as f:
        f.write(f"Sentiment social (aggiornato {time.ctime()}):\n")
        for t in titles:
            f.write(f"- {t}\n")
        f.write(f"Sentiment: {sent}\n")
        f.write(f"Volume: {volume} (media 30gg: {avg_30}, {change})\n")
        f.write(f"Intensita: {inten}/5\n")

    print(f"Social aggiornato: {sent} (volume {volume}, intensita {inten}/5, {change})", flush=True)


while True:
    save_context()
    time.sleep(600)  # 10 min
