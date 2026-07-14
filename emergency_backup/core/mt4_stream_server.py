# AI_BRIDGE - MT4 Zero-Latency Stream Server

import socket
import json
from datetime import datetime


class MT4StreamServer:
    """
    Low-latency TCP server per comunicazione live con MT4 EA.
    """

    def __init__(self, host="127.0.0.1", port=9000):

        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = None

    # =========================================
    # START SERVER
    # =========================================

    def start(self):

        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

        print("[STREAM] Waiting MT4 connection...")

        self.client, addr = self.socket.accept()

        print(f"[STREAM] MT4 connected: {addr}")

    # =========================================
    # SEND SIGNAL
    # =========================================

    def send(self, decision):

        if not self.client:
            return

        payload = self._build_payload(decision)

        message = json.dumps(payload) + "\n"

        self.client.send(message.encode("utf-8"))

        print("[STREAM] Signal sent")

    # =========================================
    # RECEIVE FEEDBACK
    # =========================================

    def receive_feedback(self):

        if not self.client:
            return None

        try:
            data = self.client.recv(1024).decode("utf-8")

            if not data:
                return None

            return json.loads(data.strip())

        except:
            return None

    # =========================================
    # BUILD MESSAGE
    # =========================================

    def _build_payload(self, decision):

        req = decision.get("request", {})

        best = decision.get("decision", {})

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": req.get("metadata", {}).get("symbol", "EURUSD"),
            "action": best.get("action", "NO_OP"),
            "lot": req.get("metadata", {}).get("lot", 0.01),
            "sl": req.get("metadata", {}).get("sl", 0),
            "tp": req.get("metadata", {}).get("tp", 0),
            "strategy": best.get("strategy", "unknown"),
            "allowed": decision.get("allowed", False)
        }
