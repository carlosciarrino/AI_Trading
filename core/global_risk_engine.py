# AI_BRIDGE - Global Risk Engine (Institutional)

class GlobalRiskEngine:

    def __init__(self):

        self.max_portfolio_risk = 0.05
        self.max_drawdown = 0.20
        self.current_exposure = 0

    # =========================================
    # VALIDATE TRADE
    # =========================================

    def approve(self, portfolio_state, trade):

        exposure = portfolio_state.get("exposure", 0)
        drawdown = portfolio_state.get("drawdown", 0)

        if drawdown > self.max_drawdown:
            return False, "MAX_DRAWDOWN_BLOCK"

        if exposure > 10:
            return False, "MAX_EXPOSURE_BLOCK"

        if trade.get("risk", 0) > self.max_portfolio_risk:
            return False, "RISK_LIMIT_BLOCK"

        return True, "APPROVED"
