import os, json, subprocess, logging, requests, feedparser
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

CHANNELS_FILE = "config/youtube_channels.json"
OUTPUT_FILE = "docs/research/YOUTUBE_SCOUT.md"
SEEN_FILE = "config/youtube_seen.json"

def load_channels():
    if not os.path.exists(CHANNELS_FILE):
        logger.error(f"File {CHANNELS_FILE} non trovato. Esegui prima channel_resolver.py")
        return {}
    with open(CHANNELS_FILE) as f:
        return json.load(f)

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return json.load(f)
    return {}

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=2)

def get_new_videos(rss_url, seen_ids):
    """Legge il feed RSS e restituisce i video non ancora visti."""
    try:
        feed = feedparser.parse(rss_url)
        new_videos = []
        for entry in feed.entries:
            vid = entry.get("yt_videoid")
            if vid and vid not in seen_ids:
                new_videos.append({
                    "video_id": vid,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published
                })
        return new_videos
    except Exception as e:
        logger.error(f"Errore RSS: {e}")
        return []

def get_transcript(video_id):
    """Scarica la trascrizione del video con yt-dlp."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--write-auto-sub", "--sub-lang", "it,en", "--skip-download", 
             "--print", "title", "-o", "/tmp/%(id)s.%(ext)s", 
             f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=120
        )
        # Cerca file di sottotitoli
        for ext in ["it.vtt", "en.vtt"]:
            path = f"/tmp/{video_id}.{ext}"
            if os.path.exists(path):
                with open(path) as f:
                    return f.read()[:5000]  # Primi 5000 caratteri
        return ""
    except Exception as e:
        logger.error(f"Errore trascrizione {video_id}: {e}")
        return ""

def summarize_with_ollama(text, title):
    """Riassume il testo con Ollama."""
    if not text:
        return "Trascrizione non disponibile."
    prompt = f"""Riassumi questo video YouTube in 5 punti chiave. Titolo: {title}
    
Testo:
{text[:3000]}

Riassunto (5 punti):"""
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "tinyllama", "prompt": prompt, "stream": False},
            timeout=60
        )
        if resp.status_code == 200:
            return resp.json().get("response", "")
    except Exception as e:
        logger.error(f"Errore Ollama: {e}")
    return "Riassunto non disponibile."

def send_telegram(text):
    token = "8928323847:AAGpoYGzlnAN39q-VM0O4ZlgrbLFXLiEzwk"
    chat_file = os.path.expanduser("~/.telegram_chat_id")
    if not os.path.exists(chat_file):
        return
    with open(chat_file) as f:
        chat_id = f.read().strip()
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text[:4000]},
            timeout=10
        )
    except:
        pass

def main():
    channels = load_channels()
    seen = load_seen()
    new_videos_found = []

    for name, info in channels.items():
        rss_url = info.get("rss_url")
        if not rss_url:
            continue
        logger.info(f"Controllo {name}...")
        seen_ids = set(seen.get(name, []))
        new_videos = get_new_videos(rss_url, seen_ids)
        for v in new_videos:
            logger.info(f"  🆕 {v['title']}")
            transcript = get_transcript(v["video_id"])
            summary = summarize_with_ollama(transcript, v["title"])
            new_videos_found.append({
                "channel": name,
                **v,
                "summary": summary
            })
            seen_ids.add(v["video_id"])
        seen[name] = list(seen_ids)

    save_seen(seen)

    if new_videos_found:
        # Scrivi report
        os.makedirs("docs/research", exist_ok=True)
        with open(OUTPUT_FILE, "a") as f:
            f.write(f"\n\n## Aggiornamento {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            for v in new_videos_found:
                f.write(f"\n### [{v['channel']}] {v['title']}\n")
                f.write(f"Link: {v['link']}\n")
                f.write(f"Pubblicato: {v['published']}\n\n")
                f.write(f"{v['summary']}\n")
        
        # Invia a Telegram
        report = f"📹 *YouTube Scout* - {len(new_videos_found)} nuovi video\n\n"
        for v in new_videos_found[:5]:
            report += f"• [{v['channel']}] {v['title'][:60]}\n"
        send_telegram(report)
        logger.info(f"✅ {len(new_videos_found)} nuovi video trovati e salvati.")
    else:
        logger.info("Nessun nuovo video.")

if __name__ == "__main__":
    main()
