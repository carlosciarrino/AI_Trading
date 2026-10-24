#!/usr/bin/env python3
"""scouting_agent.py - Cerca novita' su GitHub/HF, scrive docs/NOVITA_ESTERNE.md"""
import requests, time
from datetime import datetime

OUTPUT = "/home/carlo/AI_Trading/docs/NOVITA_ESTERNE.md"
HEADERS = {"User-Agent": "AI_Trading-Scouting/1.0"}

def get_github_trending():
    try:
        r = requests.get("https://api.github.com/search/repositories",
                         params={"q": "language:python created:>2026-10-01",
                                 "sort": "stars", "order": "desc", "per_page": 5},
                         headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return [(it["full_name"], it["html_url"], it.get("description", "")) for it in r.json().get("items", [])]
    except:
        pass
    return []

def get_hf_trending():
    try:
        r = requests.get("https://huggingface.co/api/models",
                         params={"sort": "trending", "limit": 5},
                         headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return [(m["modelId"], f"https://huggingface.co/{m['modelId']}") for m in r.json()]
    except:
        pass
    return []

def write_report(gh, hf):
    with open(OUTPUT, "w") as f:
        f.write(f"# NOVITA' ESTERNE (aggiornato {datetime.now().isoformat()})\n\n")
        f.write("## GitHub Trending (Python, ultimi 30 giorni)\n\n")
        for name, url, desc in gh:
            f.write(f"- **{name}** — {desc or 'nessuna descrizione'} ({url})\n")
        f.write("\n## Hugging Face Trending\n\n")
        for name, url in hf:
            f.write(f"- **{name}** — {url}\n")
        f.write("\n---\nReport generato da scouting_agent.py. Da rivedere in chat.\n")

def main():
    gh = get_github_trending()
    hf = get_hf_trending()
    write_report(gh, hf)
    print(f"[scouting] {len(gh)} repo GitHub, {len(hf)} modelli HF", flush=True)

if __name__ == "__main__":
    main()
