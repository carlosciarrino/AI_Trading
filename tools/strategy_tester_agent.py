import sys, time, subprocess, json, logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def run_backtest():
    logger.info("Avvio backtest...")
    result = subprocess.run(["python3", "tools/auto_backtest.py"], capture_output=True, text=True)
    logger.info(result.stdout)
    if result.stderr:
        logger.error(result.stderr)
    return result.returncode == 0

def check_drawdown(report_file):
    # Legge l'ultimo report e controlla il drawdown massimo
    with open(report_file, 'r') as f:
        data = json.load(f)
    dd = data.get('max_drawdown', 0)
    if dd > 10:
        logger.warning(f"⚠️ Drawdown > 10%: {dd:.2f}%")
        # Qui si può inviare un alert (telegram, email, file)
    return dd

if __name__ == "__main__":
    logger.info("Strategy Tester Agent avviato")
    if run_backtest():
        report_file = "reports/latest.json"
        if os.path.exists(report_file):
            check_drawdown(report_file)
    logger.info("Strategy Tester Agent completato")
