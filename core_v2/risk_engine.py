"""Risk engine for AI_BRIDGE V2.

The risk engine validates trading decisions before they are executed.
It provides a stable interface for future portfolio and money management
logic while keeping the initial implementation intentionally simple.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass

from core_v2.decision_engine import DecisionResult


@dataclass(frozen=True)
class RiskLimits:
    """Configured trading limits."""

    max_risk_per_trade: float
    max_daily_loss: float
    max_open_positions: int


@dataclass
class PortfolioState:
    """Current portfolio status."""

    open_positions: int = 0
    daily_loss_percent: float = 0.0
    emergency_stop: bool = False


@dataclass
class RiskEvaluation:
    """Result of the risk validation."""

    approved: bool
    reason: str


class RiskEngine:
    """AI_BRIDGE V2 risk validation engine."""

    def __init__(
        self,
        limits: RiskLimits,
        portfolio: PortfolioState | None = None,
    ) -> None:
        self._limits = limits
        self._portfolio = portfolio or PortfolioState()

    def evaluate(self, decision: DecisionResult) -> RiskEvaluation:
        """Validate a decision against configured limits."""

        if self._portfolio.emergency_stop:
            return RiskEvaluation(False, "Emergency stop is active.")

        if (
            self._portfolio.daily_loss_percent
            >= self._limits.max_daily_loss
        ):
            return RiskEvaluation(False, "Daily loss limit reached.")

        if (
            self._portfolio.open_positions
            >= self._limits.max_open_positions
        ):
            return RiskEvaluation(False, "Maximum open positions reached.")

        if decision.confidence <= 0.0:
            return RiskEvaluation(False, "Decision confidence is zero.")

        return RiskEvaluation(True, "Risk validation passed.")

    def portfolio(self) -> PortfolioState:
        """Return the current portfolio state."""

        return self._portfolio

    def limits(self) -> RiskLimits:
        """Return configured limits."""

        return self._limits
