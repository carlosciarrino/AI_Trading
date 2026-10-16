import json, os, logging
from pathlib import Path

logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self, config_file='risk_config.json'):
        self.shared_dir = Path(os.path.expanduser('~/mt4_shared'))
        self.config = self.load_config(config_file)
        self.max_drawdown_pct = self.config.get('max_drawdown_pct', 10)
        self.max_risk_per_trade = self.config.get('max_risk_per_trade', 0.02)
        self.equity = self.get_equity()

    def load_config(self, config_file):
        default = {'max_drawdown_pct': 10, 'max_risk_per_trade': 0.02}
        if os.path.exists(config_file):
            with open(config_file) as f:
                try:
                    return json.load(f)
                except:
                    return default
        with open(config_file, 'w') as f:
            json.dump(default, f, indent=2)
        return default

    def get_equity(self):
        orders_file = self.shared_dir / 'orders.json'
        if not orders_file.exists():
            return 10000
        with open(orders_file) as f:
            try:
                orders = json.load(f)
                # Stima equity basata su ordini chiusi (semplice)
                return 10000 + sum(o.get('pnl', 0) for o in orders if 'pnl' in o)
            except:
                return 10000

    def check(self, signal, price, sl):
        # Calcola drawdown attuale
        equity = self.get_equity()
        # Simula drawdown massimo (semplificato)
        if equity < 10000 * (1 - self.max_drawdown_pct/100):
            logger.warning(f"Drawdown > {self.max_drawdown_pct}%, equity {equity:.2f}")
            return False
        # Controlla rischio per trade
        risk = abs(price - sl) / price
        if risk > self.max_risk_per_trade:
            logger.warning(f"Rischio {risk*100:.2f}% > {self.max_risk_per_trade*100}%")
            return False
        return True
