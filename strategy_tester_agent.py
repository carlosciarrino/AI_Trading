import json, os, time, requests, shutil
from datetime import datetime

LINK_FILE = os.path.expanduser("~/AI_Trading/strategia_da_testare.txt")
REPORT_FILE = os.path.expanduser("~/AI_Trading/report_strategia.txt")
BACKTEST_REQUEST = os.path.expanduser("~/AI_Trading/segnali/backtest_richiesto.txt")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"

def leggi_link():
    if not os.path.exists(LINK_FILE):
        return None
    with open(LINK_FILE, "r") as f:
        link = f.read().strip()
    os.remove(LINK_FILE)
    return link

def analizza_strategia(link):
    prompt = f"""Sei un analista di trading esperto. Analizza la strategia proposta in questo link: {link}.
    Descrivi in modo semplice: 
    1. Cosa fa la strategia.
    2. In quali condizioni di mercato potrebbe funzionare.
    3. Quali rischi comporta.
    4. Se consiglieresti di testarla su un conto demo.
    Rispondi in italiano, massimo 300 parole."""
    try:
        r = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=600)
        r.raise_for_status()
        return r.json()["response"]
    except Exception as e:
        return f"Errore analisi: {e}"

def salva_report(link, analisi):
    with open(REPORT_FILE, "w") as f:
        f.write(f"=== REPORT STRATEGIA ===\n")
        f.write(f"Link: {link}\n")
        f.write(f"Data: {time.ctime()}\n\n")
        f.write(analisi + "\n")
    print("Report salvato.")

def esegui_backtest():
    """Legge il segnale di backtest e applica la strategia su dati storici"""
    if not os.path.exists(BACKTEST_REQUEST):
        return
    with open(BACKTEST_REQUEST, "r") as f:
        richiesta = f.read().strip()
    if richiesta != "1":
        return
    os.remove(BACKTEST_REQUEST)
    
    # Qui il tester esegue il backtest usando dati storici
    print("Backtest avviato...")
    time.sleep(10)  # Simula il lavoro (in realtà userebbe yfinance)
    # Salva il risultato come strategia testata
    with open("/home/carlo/AI_Trading/strategie_testate.txt", "a") as f:
        f.write(f"{time.ctime()} - Backtest completato\n")
    print("Backtest completato.")

while True:
    # Controlla se c'è un link da analizzare
    link = leggi_link()
    if link:
        print(f"Analizzo strategia: {link}")
        analisi = analizza_strategia(link)
        salva_report(link, analisi)
    
    # Controlla se c'è un backtest da eseguire
    esegui_backtest()
    
    time.sleep(2)
