import feedparser, time, json, os, requests
from datetime import datetime

CONFIG_PATH = os.path.expanduser("~/AI_Trading/config.json")
CONTEXT_PATH = os.path.expanduser("~/AI_Trading/youtube_context.txt")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"

def is_night():
    """True se orario tra 22:00 e 06:00 (ora locale)."""
    h = datetime.now().hour
    return h >= 22 or h < 6

def get_channels():
    try:
        with open(CONFIG_PATH) as f:
            config = json.load(f)
        return config.get("youtube_channels", ["UCqJ-XoO6j2Z2fI1lUe8U5Q"])
    except:
        return ["UCqJ-XoO6j2Z2fI1lUe8U5Q"]

def fetch_videos(channel_id):
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        feed = feedparser.parse(feed_url)
        return [entry.title for entry in feed.entries[:10]]
    except Exception as e:
        print(f"Errore fetch: {e}")
        return []

def analyze_sentiment(titles):
    if not titles:
        return "Nessun video."
    text = " ".join(titles)
    prompt = f"Analizza il sentiment di questi titoli di video finanziari. Rispondi con: positivo, negativo o neutro. Titoli: {text}"
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False, "options": {"num_predict": 20}}, timeout=30)
        r.raise_for_status()
        return r.json()["response"].strip()
    except Exception as e:
        return f"Errore AI: {e}"

def save_context():
    if not is_night():
        print("Orario diurno. In attesa della notte...", flush=True)
        return
    channels = get_channels()
    all_titles = []
    for ch in channels:
        all_titles.extend(fetch_videos(ch))
    sentiment = analyze_sentiment(all_titles)
    with open(CONTEXT_PATH, "w") as f:
        f.write(f"Analisi YouTube/Instagram (agg. {datetime.now()}):\n")
        for t in all_titles[:10]:
            f.write(f"- {t}\n")
        f.write(f"\nSentiment: {sentiment}\n")
    print(f"Contesto YouTube aggiornato (notturno): {sentiment}", flush=True)

while True:
    save_context()
    time.sleep(1800)  # 30 minuti
