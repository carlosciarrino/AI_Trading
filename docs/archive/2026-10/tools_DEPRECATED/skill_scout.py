import requests, json, logging, subprocess
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def search_github(query="trading skill forex", limit=5):
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": limit}
    try:
        r = requests.get(url, params=params, headers={"Accept": "application/json"})
        data = r.json()
        results = []
        for item in data.get("items", []):
            results.append({
                "name": item["name"],
                "url": item["html_url"],
                "stars": item["stargazers_count"],
                "description": item["description"]
            })
        return results
    except Exception as e:
        logger.error(f"Errore GitHub: {e}")
        return []

def main():
    results = search_github()
    logger.info(f"Trovati {len(results)} repository")
    for r in results:
        logger.info(f"- {r['name']} ({r['stars']}⭐): {r['url']}")
    return results

if __name__ == "__main__":
    main()
