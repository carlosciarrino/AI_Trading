# AI_BRIDGE - Execution Controller (HARDENED CORE)

from datetime import datetime
import hashlib
import json
import os


class ExecutionController:
    """
    Punto centrale tra AI e MT4.
    Garantisce coerenza, stato e sicurezza.
    """

    def __init__(self, bridge_path="mt4_signal.json"):

        self.bridge_path = bridge_path
        self.last_hash = None

    # =========================================
    # SEND SAFE SIGNAL
    # =========================================

    def send(self, decision):

        payload = self._normalize(decision)

        raw = json.dumps(payload, sort_keys=True)
        checksum = self._hash(raw)

        envelope = {
            "data": payload,
            "checksum": checksum,
            "timestamp": datetime.utcnow().isoformat()
        }

        temp_file = self.bridge_path + ".tmp"

        with open(temp_file, "w") as f:
            json.dump(envelope, f, indent=2)

        os.replace(temp_file, self.bridge_path)

        print("[EXECUTION] Safe signal sent")

    # =========================================
    # NORMALIZATION
    # =========================================

    def _normalize(self, decision):

        req = decision.get("request", {})
        best = decision.get("decision", {})

        return {
            "symbol": req.get("metadata", {}).get("symbol", "EURUSD"),
            "action": best.get("action", "NO_OP"),
            "lot": req.get("metadata", {}).get("lot", 0.01),
            "strategy": best.get("strategy", "unknown"),
            "allowed": decision.get("allowed", False)
        }

    # =========================================
    # CHECKSUM
    # =========================================

    def _hash(self, data):

        return hashlib.sha256(data.encode()).hexdigest()
