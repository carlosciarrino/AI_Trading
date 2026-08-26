import os, json, time, logging
from pathlib import Path

class MT4Bridge:
    def __init__(self, config=None):
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        self.shared_dir = Path(self.config.get('mt4_shared_dir', os.path.expanduser('~/mt4_shared')))
        self.shared_dir.mkdir(exist_ok=True)

    def connect(self):
        self.logger.info("MT4 Bridge connected")
        return True

    def disconnect(self):
        self.logger.info("MT4 Bridge disconnected")
        return True

    def get_positions(self):
        """Legge le posizioni aperte dal file (simulato)"""
        pos_file = self.shared_dir / 'positions.json'
        if pos_file.exists():
            with open(pos_file) as f:
                try:
                    return json.load(f)
                except:
                    return []
        return []

    def get_orders(self):
        """Legge tutti gli ordini dal file"""
        orders_file = self.shared_dir / 'orders.json'
        if orders_file.exists():
            with open(orders_file) as f:
                try:
                    return json.load(f)
                except:
                    return []
        return []

    def place_order(self, action, lots, price, sl, tp):
        order = {
            'action': action,
            'lots': lots,
            'price': price,
            'sl': sl,
            'tp': tp,
            'time': time.time(),
            'status': 'open',
            'close_price': None,
            'pnl': 0
        }
        orders = self.get_orders()
        orders.append(order)
        with open(self.shared_dir / 'orders.json', 'w') as f:
            json.dump(orders, f, indent=2)
        self.logger.info(f"Order {action} {lots} @ {price}")
        return {'order_id': len(orders)-1}

    def close_order(self, order_id, close_price):
        orders = self.get_orders()
        if order_id < len(orders):
            orders[order_id]['status'] = 'closed'
            orders[order_id]['close_price'] = close_price
            entry = orders[order_id]['price']
            lots = orders[order_id]['lots']
            if orders[order_id]['action'] == 'buy':
                pnl = (close_price - entry) * lots * 100000
            else:
                pnl = (entry - close_price) * lots * 100000
            orders[order_id]['pnl'] = round(pnl, 2)
            with open(self.shared_dir / 'orders.json', 'w') as f:
                json.dump(orders, f, indent=2)
            return True
        return False
