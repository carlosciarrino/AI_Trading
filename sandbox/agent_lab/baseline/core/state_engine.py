# AI_BRIDGE - State Engine

from datetime import datetime


class StateEngine:
    """
    Gestisce lo stato globale del sistema di trading.
    """

    def __init__(self):

        self.state = "SAFE"

        self.states = {
            "SAFE",
            "ACTIVE",
            "HIGH_RISK",
            "RECOVERY",
            "PAUSED"
        }

        self.state_history = []

    # =========================================
    # UPDATE STATE
    # =========================================

    def update(self, portfolio_metrics):

        drawdown = portfolio_metrics.get("drawdown", 0)
        exposure = portfolio_metrics.get("exposure", 0)
        volatility = portfolio_metrics.get("volatility", 1)

        new_state = self._decide_state(drawdown, exposure, volatility)

        if new_state != self.state:

            self.state = new_state

            self.state_history.append({
                "state": new_state,
                "timestamp": datetime.utcnow().isoformat()
            })

            print(f"[STATE_ENGINE] STATE CHANGED → {new_state}")

        return self.state

    # =========================================
    # LOGIC ENGINE
    # =========================================

    def _decide_state(self, drawdown, exposure, volatility):

        if drawdown > 0.30:
            return "PAUSED"

        if drawdown > 0.20:
            return "RECOVERY"

        if volatility > 3 or exposure > 5:
            return "HIGH_RISK"

        if volatility > 1.5:
            return "ACTIVE"

        return "SAFE"

    # =========================================
    # CHECK IF TRADING ALLOWED
    # =========================================

    def can_trade(self):

        return self.state in {"SAFE", "ACTIVE"}
