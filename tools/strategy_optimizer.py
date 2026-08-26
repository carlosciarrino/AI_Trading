import os, json, subprocess, itertools, time, logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

ASSETS = ["GBPUSD", "XAUUSD"]
TIMEFRAMES = ["15min", "1h", "4h"]
PARAMS = {
    'sl_ratio': [1.0, 1.5, 2.0],
    'tp_ratio': [1.0, 1.5, 2.0],
    'atr_period': [10, 14, 20],
}
INDICATORS = ["none", "rsi", "volume", "trend"]

def run_backtest(asset, timeframe, params, indicator):
    # Modifica il file della strategia con i parametri e indicatori
    strategy_file = "/home/carlo/AI_Trading/strategies/three_candles_simple.py"
    with open(strategy_file, 'r') as f:
        content = f.read()
    # Sostituisci parametri
    content = content.replace("params = (", f"params = (('sl_ratio', {params['sl_ratio']}), ('tp_ratio', {params['tp_ratio']}), ('atr_period', {params['atr_period']}), ")
    # Aggiungi indicatori (semplice simulazione)
    if indicator == "rsi":
        content = content.replace("def __init__(self):", "def __init__(self):\n        self.rsi = bt.indicators.RSI(self.data.close, period=14)")
        # Aggiungi filtro RSI nel next
    # Salva e esegui backtest
    with open(strategy_file, 'w') as f:
        f.write(content)
    cmd = f"cd /home/carlo/AI_Trading && source ~/AI_Trading_Agents/venv/bin/activate && python3 -c \"import sys; sys.path.insert(0, '.'); from backtest_multi import run_backtest; print(run_backtest('{asset}', '{timeframe}'))\""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    best = {'profit': -999999, 'params': None}
    for asset in ASSETS:
        for timeframe in TIMEFRAMES:
            for params in itertools.product(PARAMS['sl_ratio'], PARAMS['tp_ratio'], PARAMS['atr_period']):
                for indicator in INDICATORS:
                    p = {'sl_ratio': params[0], 'tp_ratio': params[1], 'atr_period': params[2]}
                    profit = run_backtest(asset, timeframe, p, indicator)
                    if profit and float(profit) > best['profit']:
                        best['profit'] = float(profit)
                        best['params'] = {'asset': asset, 'timeframe': timeframe, 'params': p, 'indicator': indicator}
                        logger.info(f"✅ Nuovo best: {best}")
    logger.info(f"🏆 Miglior combinazione: {best}")

if __name__ == "__main__":
    main()
