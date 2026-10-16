# AI_BRIDGE - Portfolio Risk Engine

class PortfolioRiskEngine:
    """
    Controllo rischio globale del portafoglio.
    """

    def __init__(self):

        self.max_exposure = 5
        self.max_drawdown = 0.25
        self.max_risk_per_trade = 0.02

        self.trades = []

    # =========================================
    # REGISTER TRADE
    # =========================================

    def register_trade(self, trade):

        self.trades.append(trade)

    # =========================================
    # METRICS
    # =========================================

    def compute_metrics(self):

        open_trades = [t for t in self.trades if t["status"] == "OPEN"]
        closed_trades = [t for t in self.trades if t["status"] == "CLOSED"]

        exposure = len(open_trades)

        equity = 1000
        pnl = sum(t.get("profit", 0) for t in closed_trades)

        peak = 1000
        equity_curve = peak + pnl

        drawdown = max(0, (peak - equity_curve) / peak)

        volatility = self._estimate_volatility(closed_trades)

        return {
            "exposure": exposure,
            "drawdown": drawdown,
            "volatility": volatility,
            "equity": equity_curve
        }

    # =========================================
    # VOLATILITY MODEL (SEMPLICE)
    # =========================================

    def _estimate_volatility(self, trades):

        if len(trades) < 2:
            return 1

        profits = [t.get("profit", 0) for t in trades]

        avg = sum(profits) / len(profits)

        variance = sum((p - avg) ** 2 for p in profits) / len(profits)

        return variance ** 0.5
