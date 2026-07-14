# AI_BRIDGE - Persistence Manager (PRODUCTION LAYER)

import json
import os
from datetime import datetime


class PersistenceManager:
    """
    Salva e recupera stato del sistema in modo sicuro.
    """

    def __init__(self, base_path="storage"):

        self.base_path = base_path

        os.makedirs(self.base_path, exist_ok=True)

        self.decision_log = os.path.join(self.base_path, "decisions.jsonl")
        self.trade_log = os.path.join(self.base_path, "trades.jsonl")
        self.state_file = os.path.join(self.base_path, "system_state.json")

    # =========================================
    # SAVE DECISION
    # =========================================

    def save_decision(self, decision):

        self._append(self.decision_log, decision)

    # =========================================
    # SAVE TRADE
    # =========================================

    def save_trade(self, trade):

        self._append(self.trade_log, trade)

    # =========================================
    # SAVE STATE SNAPSHOT
    # =========================================

    def save_state(self, state):

        state["timestamp"] = datetime.utcnow().isoformat()

        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)

    # =========================================
    # LOAD STATE
    # =========================================

    def load_state(self):

        if not os.path.exists(self.state_file):
            return None

        with open(self.state_file, "r") as f:
            return json.load(f)

    # =========================================
    # INTERNAL APPEND
    # =========================================

    def _append(self, file_path, data):

        data["timestamp"] = datetime.utcnow().isoformat()

        with open(file_path, "a") as f:
            f.write(json.dumps(data) + "\n")
