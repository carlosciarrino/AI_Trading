import requests
from bs4 import BeautifulSoup
import json
import logging
import os
from datetime import datetime
import random

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def fetch_tiktok_trends():
    """
    Recupera i trending topic/hashtag da TikTok Creative Center.
    Questo è un esempio semplificato; la struttura effettiva del sito potrebbe essere diversa.
    """
    url = "https://ads.tiktok.com/business/creativecenter"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        trends = []
        # Tentativo di estrarre i trending topic/hashtag
        # Cerchiamo elementi che potrebbero contenere i trending
        for item in soup.find_all('div', class_='trend-item'):
            trends.append(item.get_text(strip=True))
        
        if not trends:
            logger.warning("Nessun trending trovato su TikTok Creative Center, usando dati di esempio")
            trends = ["#example1", "#example2", "#example3"]
        
        logger.info(f"Trovati {len(trends)} trending da TikTok: {trends}")
        return trends
    
    except Exception as e:
        logger.error(f"Errore nel recupero dei trending di TikTok: {e}")
        return []

def fetch_google_trends():
    """
    Recupera i trending topic da Google Trends.
    Google Trends non ha una semplice API pubblica; per semplicità, restituiamo un elenco di tendenza fittizio.
    """
    trends = ["technology", "health", "sports", "entertainment", "politics"]
    logger.info("Usando dati di tendenza fittizi per Google Trends")
    return trends

def calculate_virality_score(trend):
    """
    Calcola uno score di viralità (0-100) per un dato trend.
    Questo è un esempio semplificato; in uno scenario reale, potresti usare
    metriche come volume di ricerche, crescita, engagement, ecc.
    """
    score = random.randint(0, 100)
    logger.debug(f"Calcolato score di viralità per {trend}: {score}")
    return score

def main():
    logger.info("Avvio dello scanner di tendenza")
    
    # Recupera i trending da entrambe le fonti
    tiktok_trends = fetch_tiktok_trends()
    google_trends = fetch_google_trends()
    
    # Combina e rimuovi duplicati
    combined_trends = list(set(tiktok_trends + google_trends))
    
    # Calcola gli score di viralità per ogni trend
    results = []
    for trend in combined_trends:
        score = calculate_virality_score(trend)
        results.append({
            "topic": trend,
            "virality_score": score,
            "source": "tiktok" if trend in tiktok_trends else "google"
        })
    
    # Assicurati che la directory di output esista
    output_dir = "docs/research"
    os.makedirs(output_dir, exist_ok=True)
    
    # Nome del file basato sulla data odierna
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(output_dir, f"TRENDS_{today}.json")
    
    # Salva i risultati
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Risultati salvati in {output_file}")

if __name__ == "__main__":
    main()
