import requests, time
from datetime import datetime
import xml.etree.ElementTree as ET

OUTPUT = "/home/carlo/AI_Trading/docs/SCOUT_ARXIV.md"
# Cerca paper su trading, q-fin.TR (Trading and Market Microstructure)
QUERY = "http://export.arxiv.org/api/query?search_query=cat:q-fin.TR+OR+(cat:cs.LG+AND+abs:trading)&sortBy=submittedDate&sortOrder=descending&max_results=10"

def main():
    print("Inizio scouting arXiv...")
    try:
        r = requests.get(QUERY, timeout=20)
        root = ET.fromstring(r.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', ns)
    except Exception as e:
        print(f"Errore arXiv: {e}")
        entries = []

    with open(OUTPUT, "w") as f:
        f.write(f"# SCOUT ARXIV (aggiornato {datetime.now().isoformat()})\n\n")
        for entry in entries:
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            link = entry.find('atom:id', ns).text.strip()
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')[:200] + "..."
            f.write(f"### {title}\n")
            f.write(f"- **Link**: {link}\n")
            f.write(f"- **Abstract**: {summary}\n\n")
    print(f"Trovati {len(entries)} paper. Report in {OUTPUT}")

if __name__ == "__main__": main()
