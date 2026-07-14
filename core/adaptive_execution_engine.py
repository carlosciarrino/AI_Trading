# AI_BRIDGE - Adaptive Execution Engine

from datetime import datetime


class AdaptiveExecutionEngine:
    """
    Modula l'esecuzione dei trade in base a condizioni reali di mercato.
    """

    def __init__(self, event_journal=None):

        self.event_journal = event_journal

        # parametri base (ottimizzabili)
        self.base_lot = 0.01

        self.max_spread = 20          # punti
        self.max_risk_per_trade = 0.02  # 2% equity teorico

        self.kill_switch = False

    # =========================================
    # MAIN ENTRY
    # =========================================

    def evaluate(self, market_data, account_state, decision):

        if self.kill_switch:
            return self._block("KILL_SWITCH_ACTIVE", decision)

        spread = market_data.get("spread", 0)
        volatility = market_data.get("volatility", 0)

        equity = account_state.get("equity", 1000)
        balance = account_state.get("balance", 1000)
        drawdown = account_state.get("drawdown", 0)

        # =====================================
        # 1. KILL SWITCH LOGIC
        # =====================================

        if drawdown > 0.25:
            self.kill_switch = True
            return self._block("MAX_DRAWDOWN_REACHED", decision)

        # =====================================
        # 2. SPREAD FILTER
        # =====================================

        if spread > self.max_spread:
            return self._block("SPREAD_TOO_HIGH", decision)

        # =====================================
        # 3. VOLATILITY ADJUSTMENT
        # =====================================

        volatility_factor = self._volatility_factor(volatility)

        # =====================================
        # 4. LOT SIZING DYNAMICO
        # =====================================

        lot = self.base_lot * volatility_factor

        lot = self._cap_lot(lot, equity)

        # =====================================
        # 5. FINAL DECISION
        # =====================================

        enriched_decision = decision.copy()

        enriched_decision["lot"] = round(lot, 2)
        enriched_decision["allowed"] = True
        enriched_decision["execution_mode"] = "ADAPTIVE"

        self._log("EXECUTION_APPROVED", enriched_decision)

        return enriched_decision

    # =========================================
    # VOLATILITY MODEL
    # =========================================

    def _volatility_factor(self, volatility):

        if volatility < 1:
            return 1.2

        if volatility < 2:
            return 1.0

        if volatility < 3:
            return 0.7

        return 0.4

    # =========================================
    # LOT CAP SYSTEM
    # =========================================

    def _cap_lot(self, lot, equity):

        max_lot = equity * self.max_risk_per_trade / 1000

        if lot > max_lot:
            return max_lot

        return lot

    # =========================================
    # BLOCK DECISION
    # =========================================

    def _block(self, reason, decision):

        blocked = decision.copy()

        blocked["allowed"] = False
        blocked["reason"] = reason
        blocked["execution_mode"] = "BLOCKED"

        self._log("EXECUTION_BLOCKED", blocked)

        return blocked

    # =========================================
    # LOGGING
    # =========================================

    def _log(self, event_type, data):

        print(f"[ADAPTIVE_EXEC] {event_type}")

        if self.event_journal and hasattr(self.event_journal, "log_event"):
            self.event_journal.log_event({
                "type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            })
