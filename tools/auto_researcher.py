import os, json, time, logging, requests
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

REPORT_DIR = "/home/carlo/AI_Trading/docs/research"
TELEGRAM_TOKEN = "8928323847:AAGpoYGzlnAN39q-VM0O4ZlgrbLFXLiEzwk"

SOURCES = {
    "github_trending": "https://api.github.com/search/repositories?q=created:>{date}+stars:>100&sort=stars&order=desc&per_page=10",
    "huggingface": "https://huggingface.co/api/models?sort=likes&direction=-1&limit=10",
}

KEYWORDS = [
    "trading", "forex", "ai-agent", "llm-agent", "video-generation",
    "text-to-video", "dropshipping", "automation", "multi-agent",
    "social-media", "content-creation", "faceless-video"
]

def send_telegram(text):
    chat_file = os.path.expanduser("~/.telegram_chat_id")
    if not os.path.exists(chat_file):
        return
    with open(chat_file) as f:
        chat_id = f.read().strip()
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text[:4000]},
            timeout=10
        )
    except Exception as e:
        logger.error(f"Telegram: {e}")

def search_github():
    date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    results = []
    for kw in KEYWORDS[:5]:
        try:
            url = f"https://api.github.com/search/repositories?q={kw}+created:>{date}&sort=stars&order=desc&per_page=5"
            r = requests.get(url, timeout=15)
            if r.status_code != 200:
                continue
            data = r.json()
            for item in data.get("items", []):
                results.append({
                    "source": "github",
                    "keyword": kw,
                    "name": item["name"],
                    "url": item["html_url"],
                    "stars": item["stargazers_count"],
                    "description": item.get("description", ""),
                    "language": item.get("language", "")
                })
        except Exception as e:
            logger.error(f"GitHub {kw}: {e}")
    return results

def search_huggingface():
    results = []
    for kw in KEYWORDS[:3]:
        try:
            url = f"https://huggingface.co/api/models?search={kw}&sort=likes&direction=-1&limit=5"
            r = requests.get(url, timeout=15)
            if r.status_code != 200:
                continue
            for item in r.json():
                results.append({
                    "source": "huggingface",
                    "keyword": kw,
                    "name": item.get("modelId", item.get("id", "")),
                    "url": f"https://huggingface.co/{item.get('modelId', item.get('id', ''))}",
                    "stars": item.get("likes", 0),
                    "description": item.get("pipeline_tag", ""),
                })
        except Exception as e:
            logger.error(f"HF {kw}: {e}")
    return results

def save_report(items):
    os.makedirs(REPORT_DIR, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    file = os.path.join(REPORT_DIR, f"AUTO_RESEARCH_{date_str}.md")
    
    with open(file, "w") as f:
        f.write(f"# Auto-Research {date_str}\n\n")
        f.write(f"Totale: {len(items)} risultati\n\n")
        
        by_source = {}
        for item in items:
            by_source.setdefault(item["source"], []).append(item)
        
        for source, list_items in by_source.items():
            f.write(f"## {source.upper()}\n\n")
            for item in list_items:
                f.write(f"- **{item['name']}** ({item.get('stars', 0)}⭐)\n")
                f.write(f"  URL: {item['url']}\n")
                if item.get('description'):
                    f.write(f"  {item['description']}\n")
                f.write("\n")
    
    logger.info(f"Report: {file}")
    return file

def main():
    logger.info("Auto-Researcher avviato")
    items = []
    items.extend(search_github())
    items.extend(search_huggingface())
    
    if not items:
        logger.info("Nessun risultato")
        send_telegram("🔍 Auto-Research: nessun nuovo risultato.")
        return
    
    file = save_report(items)
    
    # Report Telegram
    msg = f"🔍 *Auto-Research* — {len(items)} risultati\n\n"
    for item in items[:5]:
        msg += f"• [{item['name']}]({item['url']}) ({item.get('stars', 0)}⭐)\n"
    msg += f"\nReport completo: `{file}`"
    send_telegram(msg)
    logger.info("Completato")

if __name__ == "__main__":
    main()
