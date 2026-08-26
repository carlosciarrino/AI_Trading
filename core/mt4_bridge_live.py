import os, json, time, logging
from pathlib import Path

class MT4BridgeLive:
    def __init__(self, account, password, server="FPTradingLLC-Demo"):
        self.account = account
        self.password = password
        self.server = server
        self.logger = logging.getLogger(__name__)
        self.shared_dir = Path(os.path.expanduser('~/mt4_shared'))
        self.shared_dir.mkdir(exist_ok=True)

    def connect(self):
        self.logger.info(f"Connesso a {self.server} conto {self.account}")
        return True

    def place_order(self, action, lots, price, sl, tp):
        order = {
            'action': action, 'lots': lots, 'price': price,
            'sl': sl, 'tp': tp, 'time': time.time(),
            'status': 'open', 'close_price': None, 'pnl': 0
        }
        orders_file = self.shared_dir / 'orders.json'
        orders = json.load(open(orders_file)) if orders_file.exists() else []
        orders.append(order)
        with open(orders_file, 'w') as f:
            json.dump(orders, f, indent=2)
        self.logger.info(f"Order {action} {lots} @ {price}")
        return {'order_id': len(orders)-1}

    def close_order(self, order_id, close_price):
        orders = json.load(open(self.shared_dir / 'orders.json'))
        if order_id < len(orders):
            orders[order_id]['status'] = 'closed'
            orders[order_id]['close_price'] = close_price
            entry = orders[order_id]['price']
            lots = orders[order_id]['lots']
            pnl = (close_price - entry) * lots * 100000 if orders[order_id]['action'] == 'buy' else (entry - close_price) * lots * 100000
            orders[order_id]['pnl'] = round(pnl, 2)
            with open(self.shared_dir / 'orders.json', 'w') as f:
                json.dump(orders, f, indent=2)
            return True
        return False
