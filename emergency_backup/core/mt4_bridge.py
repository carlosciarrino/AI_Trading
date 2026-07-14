# AI_BRIDGE - MT4 Bridge Layer

from datetime import datetime
import json
import os


class MT4Bridge:
    """
    Bridge semplice tra AI_BRIDGE e MT4.
    Usa file JSON come canale di comunicazione.
    """

    def __init__(self, bridge_path="mt4_bridge_signal.json"):

        self.bridge_path = bridge_path

    # =========================================
    # SEND SIGNAL TO MT4
    # =========================================

    def send_signal(self, decision):

        signal = self._build_signal(decision)

        with open(self.bridge_path, "w") as f:
            json.dump(signal, f, indent=4)

        print("[MT4_BRIDGE] Signal sent to MT4")

        return signal

    # =========================================
    # BUILD SIGNAL FORMAT
    # =========================================

    def _build_signal(self, decision):

        request = decision.get("request", {})

        action = request.get("action", "NO_OP")

        # mapping base
        mt4_action = self._map_action(action)

        signal = {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": request.get("metadata", {}).get("symbol", "EURUSD"),
            "action": mt4_action,
            "lot": request.get("metadata", {}).get("lot", 0.01),
            "sl": request.get("metadata", {}).get("sl", 0),
            "tp": request.get("metadata", {}).get("tp", 0),
            "strategy": decision.get("decision", {}).get("strategy", "unknown"),
            "allowed": decision.get("allowed", False)
        }

        return signal

    # =========================================
    # ACTION MAPPING
    # =========================================

    def _map_action(self, action):

        mapping = {
            "BUY": "BUY",
            "SELL": "SELL",
            "EXECUTE_TRADE": "BUY",
            "NO_OP": "HOLD"
        }

        return mapping.get(action, "HOLD")
