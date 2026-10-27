import os, requests
from datetime import datetime

SECRETS = os.path.expanduser("~/.config/ai_trading/secrets.env")
if os.path.exists(SECRETS):
    with open(SECRETS) as f:
        for line in f:
            if "HF_TOKEN" in line:
                os.environ["HF_TOKEN"] = line.split("=")[1].strip()

TOKEN = os.environ.get("HF_TOKEN")
HEADERS = {}
if TOKEN and TOKEN != "placeholder": HEADERS["Authorization"] = f"Bearer {TOKEN}"

OUTPUT = "/home/carlo/AI_Trading/docs/SCOUT_HF.md"

def main():
    print("Inizio scouting Hugging Face...")
    try:
        r = requests.get("https://huggingface.co/api/models",
                         params={"sort": "trendingScore", "limit": 15},
                         headers=HEADERS, timeout=15)
        models = r.json() if r.status_code == 200 else []
    except Exception as e:
        print(f"Errore HF: {e}")
        models = []

    with open(OUTPUT, "w") as f:
        f.write(f"# SCOUT HUGGING FACE (aggiornato {datetime.now().isoformat()})\n\n")
        for m in models:
            f.write(f"### {m['modelId']}\n")
            f.write(f"- **Downloads**: {m.get('downloads', 0)} | **Likes**: {m.get('likes', 0)}\n")
            f.write(f"- **Task**: {m.get('pipeline_tag', 'N/A')}\n")
            f.write(f"- **URL**: https://huggingface.co/{m['modelId']}\n\n")
    print(f"Trovati {len(models)} modelli. Report in {OUTPUT}")

if __name__ == "__main__": main()
