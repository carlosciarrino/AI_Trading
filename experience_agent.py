import json, time, os

# Percorsi
ORDERS_PATH = os.path.expanduser("~/mt4_shared/orders.json")
REPORT_PATH = os.path.expanduser("~/AI_Trading/AI_REPORT_GIORNALIERO.txt")
EXPERIENCE_PATH = os.path.expanduser("~/AI_Trading/experiences.json")

def carica_esperienze():
    try:
        with open(EXPERIENCE_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def salva_esperienze(experiences):
    with open(EXPERIENCE_PATH, "w") as f:
        json.dump(experiences, f, indent=2)

def analizza_e_impara():
    esperienze = carica_esperienze()
    
    # Leggi l'ultima operazione
    ordini = []
    try:
        with open(ORDERS_PATH, "r") as f:
            ordini = json.load(f)
    except:
        pass
    
    # Cerca le ultime operazioni chiuse o fallite
    operazioni_da_valutare = [o for o in ordini if o.get("status") == "closed"]
    
    for op in operazioni_da_valutare:
        if op.get("ticket") not in [e.get("ticket") for e in esperienze]:
            # Crea la nuova esperienza
            nuova_esperienza = {
                "ticket": op.get("ticket"),
                "azione": op.get("action"),
                "prezzo": op.get("price"),
                "pnl": op.get("pnl", 0),
                "esito": "PROFITTO" if op.get("pnl", 0) > 0 else "PERDITA",
                "data": time.time()
            }
            
            if nuova_esperienza["esito"] == "PERDITA":
                nuova_esperienza["lezione"] = "La strategia con questo tipo di parametri ha fallito. Valutare se modificare il timeframe o gli indicatori."
            
            esperienze.append(nuova_esperienza)
            print(f"Nuova esperienza registrata: {nuova_esperienza['azione']} - {nuova_esperienza['esito']}", flush=True)
    
    salva_esperienze(esperienze)
    print(f"Totale esperienze archiviate: {len(esperienze)}", flush=True)

while True:
    analizza_e_impara()
    time.sleep(3600)  # Controlla ogni ora
