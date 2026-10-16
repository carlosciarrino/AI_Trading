import requests, time, os, json

# Cerca nuove skill, framework e strategie su GitHub e altre fonti
API = "https://api.github.com/search/repositories?q={}&sort=stars&order=desc&per_page=5"
OUTPUT = os.path.expanduser("~/AI_Trading/skill_research.txt")
QUERIES = [
    "trading strategy", "ai agent framework", "llm automation",
    "forex skill", "mt4 python", "technical analysis library"
]

def fetch_skills(query):
    url = API.format(query.replace(" ", "+"))
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.json().get("items", [])
    except:
        return []

def save_results():
    with open(OUTPUT, "w") as f:
        f.write(f"=== SKILL RESEARCH - {time.ctime()} ===\n")
        for q in QUERIES:
            f.write(f"\nQuery: {q}\n")
            repos = fetch_skills(q)
            for repo in repos:
                name = repo.get("full_name", "")
                desc = repo.get("description", "No desc")[:100]
                stars = repo.get("stargazers_count", 0)
                url = repo.get("html_url", "")
                f.write(f"  - {name} (Stars: {stars})\n    {desc}\n    {url}\n")

while True:
    save_results()
    time.sleep(21600)  # ogni 6 ore
