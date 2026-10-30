import os, time, requests
from datetime import datetime, timedelta

SECRETS = os.path.expanduser("~/.config/ai_trading/secrets.env")
if os.path.exists(SECRETS):
    with open(SECRETS) as f:
        for line in f:
            if "GITHUB_TOKEN" in line:
                os.environ["GITHUB_TOKEN"] = line.split("=")[1].strip()

TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Accept": "application/vnd.github.v3+json"}
if TOKEN: HEADERS["Authorization"] = f"token {TOKEN}"

OUTPUT = "/home/carlo/AI_Trading/docs/SCOUT_GITHUB.md"
QUERIES = [
    'language:python pushed:>2026-09-01 stars:>50 trading',
    'language:python pushed:>2026-09-01 stars:>50 llm agent',
    'language:python pushed:>2026-09-01 stars:>50 mcp',
    'language:python pushed:>2026-09-01 stars:>50 topic:algorithmic-trading',
    'language:python pushed:>2026-09-01 stars:>50 topic:forex'
]

def search_github(q):
    global HEADERS
    try:
        r = requests.get("https://api.github.com/search/repositories",
                         params={"q": q, "sort": "stars", "order": "desc", "per_page": 5},
                         headers=HEADERS, timeout=15)
        if r.status_code == 401:
            print("Token GitHub invalido o scaduto. Riprovo senza token...")
            HEADERS.pop("Authorization", None)
            r = requests.get("https://api.github.com/search/repositories",
                             params={"q": q, "sort": "stars", "order": "desc", "per_page": 5},
                             headers=HEADERS, timeout=15)
        if r.status_code == 200: 
            return r.json().get("items", [])
        else:
            print(f"GitHub API ha risposto con stato {r.status_code}")
    except Exception as e: 
        print(f"Errore GitHub: {e}")
    return []

def main():
    print("Inizio scouting GitHub...")
    all_repos = {}
    for q in QUERIES:
        for item in search_github(q):
            all_repos[item["full_name"]] = item
        time.sleep(2)
    
    with open(OUTPUT, "w") as f:
        f.write(f"# SCOUT GITHUB (aggiornato {datetime.now().isoformat()})\n\n")
        for name, it in all_repos.items():
            f.write(f"### {name} (⭐ {it['stargazers_count']})\n")
            f.write(f"- **Desc**: {it.get('description', 'Nessuna')}\n")
            f.write(f"- **URL**: {it['html_url']}\n")
            f.write(f"- **Creato**: {it['created_at'][:10]}\n\n")
    print(f"Trovati {len(all_repos)} repo. Report in {OUTPUT}")

if __name__ == "__main__": main()
