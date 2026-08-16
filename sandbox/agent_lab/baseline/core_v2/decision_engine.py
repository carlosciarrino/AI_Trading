"""Decision engine for AI_BRIDGE V2.

The decision engine transforms market information into trading
decisions. This first implementation provides the common interface used
by the rest of the system while keeping the decision logic intentionally
simple.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from core_v2.market_engine import MarketEngine


class Decision(Enum):
    """Supported trading decisions."""

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass
class DecisionResult:
    """Result produced by the decision engine."""

    decision: Decision
    confidence: float
    reason: str


class DecisionEngine:
    """AI_BRIDGE V2 decision engine."""

    def __init__(self, market_engine: MarketEngine) -> None:
        self._market_engine = market_engine
        self._last_result = DecisionResult(
            decision=Decision.HOLD,
            confidence=0.0,
            reason="Engine not initialized.",
        )

    def evaluate(self) -> DecisionResult:
        """Evaluate the current market state."""

        if not self._market_engine.is_ready():
            self._last_result = DecisionResult(
                decision=Decision.HOLD,
                confidence=0.0,
                reason="Market engine is not ready.",
            )
            return self._last_result

        symbols = self._market_engine.get_symbols()

        if not symbols:
            self._last_result = DecisionResult(
                decision=Decision.HOLD,
                confidence=0.0,
                reason="No watched symbols configured.",
            )
            return self._last_result

        self._last_result = DecisionResult(
            decision=Decision.HOLD,
            confidence=0.50,
            reason=f"Monitoring {len(symbols)} symbol(s).",
        )

        return self._last_result

    def last_result(self) -> DecisionResult:
        """Return the last computed decision."""

        return self._last_result

    def reset(self) -> None:
        """Reset the engine state."""

        self._last_result = DecisionResult(
            decision=Decision.HOLD,
            confidence=0.0,
            reason="Engine reset.",
        )
