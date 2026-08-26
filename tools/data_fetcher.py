import os, json, time, logging, requests
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, config_file='data_fetcher_config.json'):
        self.config = self.load_config(config_file)
        self.data_dir = os.path.expanduser(self.config.get('data_dir', '~/AI_Trading/data/historical'))
        os.makedirs(self.data_dir, exist_ok=True)

    def load_config(self, config_file):
        default = {
            'alpha_vantage_key': os.getenv('ALPHA_VANTAGE_KEY', ''),
            'oanda_key': os.getenv('OANDA_API_KEY', ''),
            'data_dir': '~/AI_Trading/data/historical'
        }
        if os.path.exists(config_file):
            with open(config_file) as f:
                config = json.load(f)
                default.update(config)
        else:
            with open(config_file, 'w') as f:
                json.dump(default, f, indent=2)
        return default

    def fetch_alpha_vantage(self, symbol='EURUSD', interval='15min', outputsize='full'):
        """Scarica dati intraday da Alpha Vantage."""
        if not self.config['alpha_vantage_key']:
            raise ValueError("ALPHA_VANTAGE_KEY non impostata")
        url = f"https://www.alphavantage.co/query"
        params = {
            'function': 'FX_INTRADAY',
            'from_symbol': 'EUR',
            'to_symbol': 'USD',
            'interval': interval,
            'apikey': self.config['alpha_vantage_key'],
            'outputsize': outputsize,
            'datatype': 'json'
        }
        response = requests.get(url, params=params, timeout=30)
        if response.status_code != 200:
            raise Exception(f"Errore Alpha Vantage: {response.text}")
        data = response.json()
        key = f'Time Series FX ({interval})'
        if key not in data:
            raise Exception(f"Chiave non trovata: {data}")
        df = pd.DataFrame.from_dict(data[key], orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        df.columns = ['Open','High','Low','Close']
        # Salva
        filename = f"{symbol.replace('/','_')}_{interval}_{datetime.today().strftime('%Y%m%d')}.csv"
        filepath = os.path.join(self.data_dir, filename)
        df.to_csv(filepath)
        logger.info(f"Dati intraday salvati in {filepath}")
        return df

    def fetch_daily(self, symbol='EURUSD=X', start='2020-01-01', end=None):
        """Scarica dati daily da Yahoo Finance."""
        if not end:
            end = datetime.today().strftime('%Y-%m-%d')
        df = yf.download(symbol, start=start, end=end, multi_level_index=False)
        if df.empty:
            raise Exception("Nessun dato scaricato")
        df = df[['Open','High','Low','Close','Volume']]
        filename = f"{symbol.replace('=','')}_daily_{start}_{end}.csv"
        filepath = os.path.join(self.data_dir, filename)
        df.to_csv(filepath)
        logger.info(f"Dati daily salvati in {filepath}")
        return df

    def fetch_multi_timeframe(self, symbol='EURUSD', intervals=['15min','60min','4h','daily']):
        """Scarica multipli timeframe per lo stesso simbolo."""
        results = {}
        for interval in intervals:
            try:
                if interval == 'daily':
                    df = self.fetch_daily(symbol)
                else:
                    df = self.fetch_alpha_vantage(symbol, interval)
                results[interval] = df
                time.sleep(12)  # rispetta rate limit (5 richieste/minuto)
            except Exception as e:
                logger.error(f"Errore per {interval}: {e}")
        return results

if __name__ == '__main__':
    # Test rapido
    fetcher = DataFetcher()
    fetcher.fetch_daily('EURUSD=X', start='2026-06-01')
