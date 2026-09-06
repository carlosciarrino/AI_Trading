#!/usr/bin/env python3
import json, os, time, csv
from datetime import datetime, timedelta
import pytz
import requests

REPORT_FILE = "/home/carlo/AI_Trading/report_anomalie.txt"
DATA_FILE = "/home/carlo/AI_Trading/dati_storici_eurusd.csv"

def get_historical_data():
    """
    Scarica dati storici (EURUSD) da un feed gratuito o da un file locale.
    Se non esiste, usa un dataset campione (da migliorare con dati reali).
    """
    try:
        # Prova a leggere da CSV locale
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                reader = csv.DictReader(f)
                return list(reader)
        else:
            # Usa un dataset fittizio per test (poi sostituire con dati reali)
            print("⚠️ Dataset storico non trovato. Scarico campione...")
            # Simula la creazione di un dataset di esempio
            with open(DATA_FILE, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Open", "High", "Low", "Close", "Volume"])
                # Genera 100 righe fittizie
                import random
                base = 1.1000
                for i in range(100):
                    date = (datetime.now() - timedelta(days=100-i)).strftime("%Y-%m-%d")
                    close = base + random.uniform(-0.05, 0.05)
                    writer.writerow([date, close, close+0.001, close-0.001, close, random.randint(100, 10000)])
            print("✅ Dataset campione creato.")
            return []
    except Exception as e:
        print(f"Errore nel caricamento dati: {e}")
        return []

def analyze_volume_patterns(data):
    """Cerca picchi di volume anomali (senza notizie)"""
    if not data:
        return []
    anomalies = []
    # Calcola volume medio
    volumes = [float(row.get("Volume", 0)) for row in data if row.get("Volume")]
    if not volumes:
        return []
    avg_vol = sum(volumes) / len(volumes)
    for row in data:
        vol = float(row.get("Volume", 0))
        if vol > avg_vol * 2.5:
            anomalies.append({
                "date": row.get("Date", "N/A"),
                "volume": vol,
                "avg_volume": avg_vol,
                "ratio": vol / avg_vol
            })
    return anomalies

def analyze_monday_gap(data):
    """Cerca gap di apertura tra venerdì e lunedì"""
    if len(data) < 10:
        return []
    gaps = []
    for i in range(1, len(data)):
        row = data[i]
        prev = data[i-1]
        # Controlla se il giorno è lunedì
        try:
            curr_date = datetime.strptime(row.get("Date", ""), "%Y-%m-%d")
            if curr_date.weekday() == 0:  # Lunedì
                gap = float(row.get("Open", 0)) - float(prev.get("Close", 0))
                if abs(gap) > 0.001:  # > 10 pip (approssimativo)
                    gaps.append({
                        "date": row.get("Date"),
                        "gap": gap,
                        "prev_close": prev.get("Close"),
                        "open": row.get("Open")
                    })
        except:
            pass
    return gaps

def analyze_tuesday_thursday(data):
    """Cerca movimenti anomali in altri giorni (martedì-giovedì)"""
    # Semplice placeholder – da espandere
    return []

def main():
    print("Avviato Market Anomaly Researcher")
    while True:
        try:
            data = get_historical_data()
            if data:
                volume_anomalies = analyze_volume_patterns(data)
                monday_gaps = analyze_monday_gap(data)
                tue_thu_anomalies = analyze_tuesday_thursday(data)
                
                # Scrivi report
                with open(REPORT_FILE, 'w') as f:
                    f.write(f"=== REPORT ANOMALIE DI MERCATO ===\n")
                    f.write(f"Generato: {datetime.now()}\n\n")
                    
                    f.write(f"📊 VOLUME ANOMALIE (volume > 2.5x media):\n")
                    for a in volume_anomalies[:10]:
                        f.write(f"  {a['date']}: volume {a['volume']:.0f} (media {a['avg_volume']:.0f}) - ratio {a['ratio']:.2f}x\n")
                    if not volume_anomalies:
                        f.write("  Nessuna anomalia rilevata.\n")
                    
                    f.write(f"\n📈 GAP LUNEDÌ (apertura vs chiusura venerdì):\n")
                    for g in monday_gaps[:10]:
                        f.write(f"  {g['date']}: gap {g['gap']:.4f} (close: {g['prev_close']} -> open: {g['open']})\n")
                    if not monday_gaps:
                        f.write("  Nessun gap significativo.\n")
                    
                    f.write(f"\n🔍 ALTRI PATTERN (martedì-giovedì):\n")
                    if tue_thu_anomalies:
                        f.write("  Da approfondire...\n")
                    else:
                        f.write("  Nessun pattern rilevato.\n")
                
                print("✅ Report aggiornato.")
            else:
                print("⚠️ Dati non disponibili.")
        except Exception as e:
            print(f"Errore: {e}")
        time.sleep(3600)  # Esegue ogni ora

if __name__ == "__main__":
    main()
