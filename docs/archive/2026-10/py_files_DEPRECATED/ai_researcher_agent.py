import requests, time, os, json

# Sorgenti affidabili (ma non al 100%) per trovare nuove AI
SOURCES = [
    "https://huggingface.co/api/models?sort=downloads&direction=-1&limit=10",
    "https://huggingface.co/api/models?sort=trending&limit=10"
]

OUTPUT = os.path.expanduser("~/AI_Trading/ai_research.txt")

def fetch_models():
    models = []
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            data = r.json()
            for m in data:
                models.append({
                    "name": m.get("modelId", ""),
                    "downloads": m.get("downloads", 0),
                    "likes": m.get("likes", 0)
                })
        except:
            pass
    return models

def save_results():
    models = fetch_models()
    with open(OUTPUT, "w") as f:
        f.write(f"=== NUOVE AI RILEVATE - {time.ctime()} ===\n\n")
        for m in models:
            f.write(f"- {m['name']} (downloads: {m['downloads']}, likes: {m['likes']})\n")
    print("Ricerca AI completata.")

while True:
    save_results()
    time.sleep(86400)  # una volta al giorno
