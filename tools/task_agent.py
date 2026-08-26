import subprocess, time, logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        return result.stdout
    except Exception as e:
        logger.error(f"Errore: {e}")
        return ""

def backtest_multi():
    logger.info("Avvio backtest multi-asset...")
    out = run_command("cd /home/carlo/AI_Trading && python3 backtest_multi.py")
    logger.info(out[-500:])
    return out

def equity_curve():
    logger.info("Generazione equity curve...")
    run_command("cd /home/carlo/AI_Trading && python3 tools/equity_curve.py")
    logger.info("Equity curve aggiornata.")

def fetch_news():
    logger.info("Aggiornamento notizie...")
    run_command("cd /home/carlo/AI_Trading && python3 -c 'from tools.news_fetcher import get_forex_live_news; print(get_forex_live_news())'")
    logger.info("Notizie aggiornate.")

def main():
    while True:
        backtest_multi()
        equity_curve()
        fetch_news()
        logger.info("Task completati. Attendo 6 ore...")
        time.sleep(21600)  # 6 ore

if __name__ == '__main__':
    main()
