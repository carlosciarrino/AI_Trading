#!/usr/bin/env python3
"""scouting_agent.py v2 - Cerca novita' su GitHub, HuggingFace, arXiv.
Scrive docs/NOVITA_ESTERNE.md. No LLM, deterministico, CPU-only."""
import requests, time
from datetime import datetime

OUTPUT = "/home/carlo/AI_Trading/docs/NOVITA_ESTERNE.md"
HEADERS = {"User-Agent": "AI_Trading-Scouting/2.0"}


def get_github_trending():
    results = []
    try:
        r = requests.get("https://api.github.com/search/repositories",
                         params={"q": "language:python created:>2026-09-01 stars:>30",
                                 "sort": "stars", "order": "desc", "per_page": 5},
                         headers=HEADERS, timeout=15)
        if r.status_code == 200:
            for it in r.json().get("items", []):
                results.append({
                    "name": it["full_name"],
                    "url": it["html_url"],
                    "desc": (it.get("description") or "")[:150],
                    "stars": it.get("stargazers_count", 0),
                })
    except Exception as e:
        print(f"[scouting] GitHub errore: {e}", flush=True)
    return results


def get_hf_trending():
    results = []
    try:
        r = requests.get("https://huggingface.co/api/models",
                         params={"sort": "trending", "limit": 5, "direction": -1},
                         headers=HEADERS, timeout=15)
        if r.status_code == 200:
            for m in r.json():
                results.append({
                    "name": m.get("modelId", ""),
                    "url": f"https://huggingface.co/{m.get('modelId', '')}",
                    "downloads": m.get("downloads", 0),
                    "likes": m.get("likes", 0),
                })
    except Exception as e:
        print(f"[scouting] HF errore: {e}", flush=True)
    return results


def get_arxiv():
    results = []
    try:
        # Query: q-fin.TR (Trading) o cs.LG con "trading" o "agent"
        query = "cat:q-fin.TR OR abs:trading OR abs:forex"
        r = requests.get("http://export.arxiv.org/api/query",
                         params={"search_query": query, "start": 0, "max_results": 3,
                                 "sortBy": "submittedDate", "sortOrder": "descending"},
                         headers=HEADERS, timeout=15)
        if r.status_code == 200:
            # Parsing minimale XML
            import re
            entries = re.findall(r"<entry>(.*?)</entry>", r.text, re.DOTALL)
            for entry in entries:
                title = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
                link = re.search(r"<id>(.*?)</id>", entry, re.DOTALL)
                if title and link:
                    results.append({
                        "title": title.group(1).strip()[:150],
                        "url": link.group(1).strip(),
                    })
    except Exception as e:
        print(f"[scouting] arXiv errore: {e}", flush=True)
    return results


def write_report(gh, hf, arxiv):
    with open(OUTPUT, "w") as f:
        f.write(f"# NOVITA' ESTERNE (aggiornato {datetime.now().isoformat()})\n\n")
        
        f.write("## GitHub (Python, ultimi 60gg, >30 stelle)\n\n")
        if gh:
            for r in gh:
                f.write(f"- **{r['name']}** (⭐ {r['stars']}) — {r['desc']} ({r['url']})\n")
        else:
            f.write("- (nessun risultato)\n")
        
        f.write("\n## HuggingFace (trending)\n\n")
        if hf:
            for r in hf:
                f.write(f"- **{r['name']}** (downloads: {r['downloads']}, likes: {r['likes']}) — {r['url']}\n")
        else:
            f.write("- (nessun risultato)\n")
        
        f.write("\n## arXiv (q-fin.TR, trading, forex)\n\n")
        if arxiv:
            for r in arxiv:
                f.write(f"- **{r['title']}** — {r['url']}\n")
        else:
            f.write("- (nessun risultato)\n")
        
        f.write("\n---\nReport generato da scouting_agent.py v2. Da rivedere in chat.\n")


def main():
    gh = get_github_trending()
    time.sleep(1)
    hf = get_hf_trending()
    time.sleep(3)  # arXiv richiede 3 sec tra richieste
    arxiv = get_arxiv()
    write_report(gh, hf, arxiv)
    print(f"[scouting] GitHub: {len(gh)}, HF: {len(hf)}, arXiv: {len(arxiv)}", flush=True)


if __name__ == "__main__":
    main()
