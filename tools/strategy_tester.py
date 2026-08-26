import os, re, json, requests, subprocess, logging, tempfile
from datetime import datetime
from flask import request, jsonify

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def extract_rules_from_text(text):
    prompt = f"""
Sei un esperto di trading. Analizza il seguente testo e estrai le regole di una strategia.
Formato di output (JSON):
{{
  "name": "nome_strategia",
  "timeframe": "15min",
  "entry": "condizione di entrata (es. close > SMA(20))",
  "exit": "condizione di uscita (es. close < SMA(20))",
  "sl": "regola per stop loss (es. close - 1.5*ATR)",
  "tp": "regola per take profit (es. close + 2*ATR)"
}}

Testo:
{text[:3000]}
"""
    try:
        resp = requests.post("http://localhost:11434/api/generate",
                             json={"model": "llama3.2:3b", "prompt": prompt, "stream": False},
                             timeout=60)
        result = resp.json().get("response", "")
        # Estrai JSON
        match = re.search(r'\{.*\}', result, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except Exception as e:
        logger.error(f"Errore estrazione: {e}")
        return None

def generate_backtest_code(rules, symbol="EURUSD"):
    code = f"""
import backtrader as bt
import yfinance as yf

class Strategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SMA(period=20)
        self.atr = bt.indicators.ATR(period=14)

    def next(self):
        if not self.position:
            if {rules.get('entry', 'self.data.close[0] > self.sma[0]')}:
                sl = {rules.get('sl', 'self.data.close[0] - 1.5*self.atr[0]')}
                tp = {rules.get('tp', 'self.data.close[0] + 2*self.atr[0]')}
                self.buy()
        else:
            if {rules.get('exit', 'self.data.close[0] < self.sma[0]')}:
                self.close()

data = yf.download('{symbol}=X', start='2026-07-01', end='2026-08-20')
cerebro = bt.Cerebro()
cerebro.adddata(bt.feeds.PandasData(dataname=data))
cerebro.addstrategy(Strategy)
cerebro.broker.set_cash(10000)
print('Capitale iniziale:', cerebro.broker.getvalue())
cerebro.run()
print('Capitale finale:', cerebro.broker.getvalue())
"""
    return code

def test_strategy_from_link(url):
    # Scarica contenuto (semplice)
    try:
        if "youtube.com" in url or "youtu.be" in url:
            # Usa yt-dlp per trascrizione
            import yt_dlp
            ydl_opts = {'quiet': True, 'skip_download': True, 'writesubtitles': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                text = info.get('description', '') + " " + info.get('title', '')
        else:
            # PDF o testo
            import requests
            r = requests.get(url, timeout=30)
            text = r.text[:5000]
    except Exception as e:
        logger.error(f"Errore download: {e}")
        return None

    rules = extract_rules_from_text(text)
    if not rules:
        return None

    code = generate_backtest_code(rules)
    # Salva e esegui
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        tmp = f.name
    result = subprocess.run(["python3", tmp], capture_output=True, text=True, timeout=60)
    os.unlink(tmp)
    return result.stdout + result.stderr

if __name__ == "__main__":
    # Test con link
    import sys
    if len(sys.argv) > 1:
        print(test_strategy_from_link(sys.argv[1]))
