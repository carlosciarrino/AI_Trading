import json, time, os

# Percorsi
ORDERS_PATH = os.path.expanduser("~/mt4_shared/orders.json")
EXPERIENCE_PATH = os.path.expanduser("~/AI_Trading/experiences.json")

# P031: lezione generata da reflection_agent.py, non piu' generica.

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

    ordini = []
    try:
        with open(ORDERS_PATH, "r") as f:
            ordini = json.load(f)
    except:
        pass

    operazioni_da_valutare = [o for o in ordini if o.get("status") == "closed"]

    for op in operazioni_da_valutare:
        if op.get("ticket") not in [e.get("ticket") for e in esperienze]:
            nuova_esperienza = {
                "ticket": op.get("ticket"),
                "azione": op.get("action"),
                "prezzo": op.get("price"),
                "pnl": op.get("pnl", 0),
                "esito": "PROFITTO" if op.get("pnl", 0) > 0 else "PERDITA",
                "data": time.time(),
                "lezione": None,  # verra' generata da reflection_agent.py
            }
            esperienze.append(nuova_esperienza)
            print(f"Nuova esperienza registrata (lezione pending): {nuova_esperienza['azione']} - {nuova_esperienza['esito']}", flush=True)

    salva_esperienze(esperienze)
    print(f"Totale esperienze archiviate: {len(esperienze)}", flush=True)

while True:
    analizza_e_impara()
    time.sleep(3600)  # Controlla ogni ora
