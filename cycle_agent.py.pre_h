import yfinance as yf, time, os
from datetime import datetime

CYCLES_PATH = os.path.expanduser("~/AI_Trading/cycles_context.txt")

def analyze_cycles():
    try:
        df = yf.download("EURUSD=X", period="5y", interval="1d", progress=False)
        if df.empty: return
        df['Month'] = df.index.month
        monthly_avg = df.groupby('Month')['Close'].mean()
        
        with open(CYCLES_PATH, "w") as f:
            f.write(f"Analisi stagionale (ultimi 5 anni) aggiornata {datetime.now()}:\n")
            for month, avg in monthly_avg.items():
                f.write(f"- Mese {month}: media prezzo {avg:.5f}\n")
        print("Cicli storici aggiornati.")
    except Exception as e:
        print(f"Errore cicli: {e}")

while True:
    analyze_cycles()
    time.sleep(86400) # una volta al giorno
