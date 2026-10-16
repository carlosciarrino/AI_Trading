import os, sys, glob, json, pandas as pd
from datetime import datetime
sys.path.insert(0, ".")
from run_backtest_intraday import run_backtest

def find_latest_file(pattern):
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def main():
    data_dir = "data/historical"
    latest = find_latest_file(f"{data_dir}/EUR_USD_*_15min.csv")
    if not latest:
        print("Nessun dato trovato.")
        return
    print(f"📊 Backtest con {latest}")
    result = run_backtest(latest)
    report_file = f"reports/backtest_{datetime.today().strftime('%Y%m%d_%H%M')}.json"
    os.makedirs("reports", exist_ok=True)
    with open(report_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"✅ Report salvato in {report_file}")

if __name__ == "__main__":
    main()
