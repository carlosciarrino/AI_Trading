# AI_BRIDGE - Monitoring System

import time
from datetime import datetime


class MonitoringSystem:
    """
    Controlla lo stato del sistema in tempo reale.
    """

    def __init__(self):

        self.start_time = time.time()

        self.metrics = {
            "decisions": 0,
            "trades": 0,
            "blocks": 0,
            "errors": 0
        }

    # =========================================
    # UPDATE METRICS
    # =========================================

    def log_decision(self, decision):

        self.metrics["decisions"] += 1

        if not decision.get("allowed", True):
            self.metrics["blocks"] += 1

    def log_trade(self):

        self.metrics["trades"] += 1

    def log_error(self):

        self.metrics["errors"] += 1

    # =========================================
    # HEALTH CHECK
    # =========================================

    def health_check(self):

        uptime = time.time() - self.start_time

        health = {
            "uptime_sec": uptime,
            "decisions": self.metrics["decisions"],
            "trades": self.metrics["trades"],
            "blocks": self.metrics["blocks"],
            "errors": self.metrics["errors"],
            "status": self._status()
        }

        return health

    # =========================================
    # SYSTEM STATUS LOGIC
    # =========================================

    def _status(self):

        if self.metrics["errors"] > 10:
            return "UNSTABLE"

        if self.metrics["blocks"] > self.metrics["decisions"] * 0.5:
            return "RISK_BLOCK"

        return "HEALTHY"
