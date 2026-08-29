import requests, time, os

API = "https://api.github.com/search/repositories?q={}&sort=stars&order=desc&per_page=5"
OUTPUT = os.path.expanduser("~/AI_Trading/github_research.txt")
QUERIES = ["forex trading bot", "mt4 bridge", "ai trading agent", "llm trading", "sentiment analysis forex"]

def fetch_repos(query):
    url = API.format(query.replace(" ", "+"))
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.json().get("items", [])
    except:
        return []

def save_results():
    with open(OUTPUT, "w") as f:
        f.write(f"=== GITHUB RESEARCH - {time.ctime()} ===\n")
        for q in QUERIES:
            f.write(f"\nQuery: {q}\n")
            repos = fetch_repos(q)
            for repo in repos:
                name = repo.get("full_name", "")
                desc = repo.get("description", "No desc")[:100]
                stars = repo.get("stargazers_count", 0)
                url = repo.get("html_url", "")
                f.write(f"  - {name} (Stars: {stars})\n    {desc}\n    {url}\n")

while True:
    save_results()
    time.sleep(21600)  # ogni 6 ore
