import yfinance as yf
import pandas as pd
import time, os

# Percorso del file per le strategie testate
STRATEGIE_PATH = os.path.expanduser("~/AI_Trading/strategie_testate.csv")

def testa_strategia(simbolo, timeframe, indicatore):
    # Scarica dati storici
    dati = yf.download(simbolo, period="1y", interval=timeframe, progress=False)
    
    # Applica un filtro semplice (es. media mobile)
    if indicatore == "SMA":
        dati['SMA'] = dati['Close'].rolling(window=20).mean()
        # Segnale: acquisto se il prezzo supera la media
        segnale = (dati['Close'] > dati['SMA']).astype(int)
    else:
        # Default: nessuna strategia
        segnale = 0
    
    # Calcola il profitto cumulativo
    profitto = (dati['Close'].pct_change() * segnale.shift(1)).sum()
    
    return profitto

def main():
    # Strategie da testare
    strategie = [
        {"simbolo": "EURUSD=X", "timeframe": "1h", "indicatore": "SMA"},
        {"simbolo": "EURUSD=X", "timeframe": "4h", "indicatore": "SMA"},
        {"simbolo": "EURUSD=X", "timeframe": "1d", "indicatore": "SMA"}
    ]
    
    risultati = []
    for s in strategie:
        profitto = testa_strategia(s["simbolo"], s["timeframe"], s["indicatore"])
        ris = {"strategia": f"{s['indicatore']} su {s['timeframe']}", "profitto": profitto, "esito": "FUNZIONA" if profitto > 0 else "SCARTATA"}
        risultati.append(ris)
        print(f"Testata strategia {ris['strategia']}: {ris['esito']}", flush=True)
    
    # Salva il report in CSV
    df = pd.DataFrame(risultati)
    df.to_csv(STRATEGIE_PATH, index=False)
    print("Report strategie salvato.", flush=True)

while True:
    main()
    time.sleep(86400)  # Testa una volta al giorno
