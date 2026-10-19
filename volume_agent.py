import json, time, os
from datetime import datetime

# P048: legge volume_data.json (Tick Volume reale da MT4) invece di yfinance.
VOLUME_JSON = "/home/carlo/Scrivania/XM MT4/MQL4/Files/volume_data.json"
CONTEXT_PATH = "/home/carlo/AI_Trading/volume_context.txt"
HISTORY_PATH = "/home/carlo/AI_Trading/volume_history.json"


def load_history():
    try:
        with open(HISTORY_PATH) as f:
            return json.load(f)
    except:
        return []


def save_history(history):
    # tieni ultimi 100 campioni (per media)
    history = history[-100:]
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f)


def read_volume_data():
    try:
        with open(VOLUME_JSON) as f:
            return json.load(f)
    except Exception as e:
        return None


def compute_divergence(data, avg_volume):
    """Calcola divergenza prezzo-volume.
    Restituisce (divergenza, score, descrizione).
    """
    volume = data.get("volume", 0)
    volume_prev = data.get("volume_prev", 0)
    price = data.get("price", 0)
    price_prev = data.get("price_prev", 0)

    if not all([volume, volume_prev, price, price_prev]):
        return ("neutra", 0.0, "dati insufficienti")

    volume_ratio = volume / avg_volume if avg_volume > 0 else 1.0
    price_change = (price - price_prev) / price_prev

    # Divergenza
    # Prezzo su + Volume giu = debolezza (negativo)
    # Prezzo su + Volume su = forza (positivo)
    # Prezzo giu + Volume su = forza negativa (negativo)
    # Prezzo giu + Volume giu = esaurimento (positivo)
    if price_change > 0 and volume_ratio < 0.7:
        return ("negativa", -0.3, f"prezzo su, volume giu (ratio {volume_ratio:.2f})")
    if price_change > 0 and volume_ratio > 1.5:
        return ("positiva", 0.3, f"prezzo su, volume su (ratio {volume_ratio:.2f})")
    if price_change < 0 and volume_ratio > 1.5:
        return ("negativa", -0.3, f"prezzo giu, volume su (ratio {volume_ratio:.2f})")
    if price_change < 0 and volume_ratio < 0.7:
        return ("positiva", 0.3, f"prezzo giu, volume giu (esaurimento, ratio {volume_ratio:.2f})")

    return ("neutra", 0.0, f"prezzo {price_change:+.4f}, volume ratio {volume_ratio:.2f}")


def process():
    data = read_volume_data()
    if data is None:
        with open(CONTEXT_PATH, "w") as f:
            f.write("Timestamp: nessun dato\n")
            f.write("Volume ratio: 1.00\n")
            f.write("Divergenza: neutra\n")
            f.write("Punteggio: 0.00\n")
        print("[volume] volume_data.json non trovato", flush=True)
        return

    history = load_history()
    # Media volume storica (ultimi 20 campioni)
    recent = [h.get("volume", 0) for h in history[-20:] if h.get("volume", 0) > 0]
    if recent:
        avg_volume = sum(recent) / len(recent)
    else:
        # fallback: media tra current e prev
        avg_volume = (data.get("volume", 0) + data.get("volume_prev", 0)) / 2 or 1

    divergenza, score, desc = compute_divergence(data, avg_volume)

    history.append({
        "timestamp": data.get("timestamp", time.time()),
        "volume": data.get("volume", 0),
        "price": data.get("price", 0),
    })
    save_history(history)

    with open(CONTEXT_PATH, "w") as f:
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Volume: {data.get('volume', 0)} (prev {data.get('volume_prev', 0)}, media {avg_volume:.0f})\n")
        f.write(f"Price: {data.get('price', 0)} (prev {data.get('price_prev', 0)})\n")
        f.write(f"Volume ratio: {data.get('volume', 0) / avg_volume:.2f}\n")
        f.write(f"Divergenza: {divergenza}\n")
        f.write(f"Dettaglio: {desc}\n")
        f.write(f"Punteggio: {score:.2f}\n")

    print(f"[volume] {divergenza} (score {score:+.2f}): {desc}", flush=True)


if __name__ == "__main__":
    while True:
        try:
            process()
        except Exception as e:
            print(f"[volume] Errore: {e}", flush=True)
        time.sleep(60)  # ogni minuto
