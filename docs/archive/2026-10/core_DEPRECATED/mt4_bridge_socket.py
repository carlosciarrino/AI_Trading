import socket, json, logging, time
from pathlib import Path

logger = logging.getLogger(__name__)

class MT4BridgeSocket:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            logger.info(f"Connected to MT4 bridge at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Socket connect failed: {e}")
            return False

    def place_order(self, action, lots, price, sl, tp):
        if not self.sock:
            return None
        order = {'action': action, 'lots': lots, 'price': price, 'sl': sl, 'tp': tp}
        try:
            self.sock.send((json.dumps(order) + '\n').encode())
            resp = self.sock.recv(1024).decode()
            return json.loads(resp)
        except Exception as e:
            logger.error(f"Order failed: {e}")
            return None

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = None
