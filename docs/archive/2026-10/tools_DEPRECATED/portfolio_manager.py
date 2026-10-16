import logging

logger = logging.getLogger(__name__)

class PortfolioManager:
    def __init__(self, max_risk_per_trade=0.02, max_drawdown=0.10):
        self.max_risk_per_trade = max_risk_per_trade
        self.max_drawdown = max_drawdown
        self.equity = 10000

    def validate(self, signal, price, sl, tp, positions):
        # 1. Controlla rischio per trade
        risk = abs(price - sl) / price
        if risk > self.max_risk_per_trade:
            logger.warning(f"Rischio {risk:.2f}% > {self.max_risk_per_trade*100}%")
            return False, "Rischio troppo alto"

        # 2. Controlla drawdown massimo
        total_pnl = sum(p.get('pnl', 0) for p in positions)
        if total_pnl < -self.max_drawdown * self.equity:
            logger.warning(f"Drawdown {abs(total_pnl):.2f} > {self.max_drawdown*100}%")
            return False, "Drawdown massimo raggiunto"

        # 3. Controlla numero di posizioni aperte
        if len(positions) >= 3:
            logger.warning("Troppe posizioni aperte (max 3)")
            return False, "Troppe posizioni aperte"

        return True, "Validato"
