"""Execution engine for AI_BRIDGE V2.

The execution engine receives a validated trading decision from the
risk engine and simulates its execution.

This first implementation intentionally performs only simulated
executions. It provides a stable interface that future broker adapters
(MT4, MT5, FIX, etc.) will implement.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass

from core_v2.decision_engine import Decision
from core_v2.risk_engine import RiskEvaluation


@dataclass
class ExecutionRequest:
    """Execution request generated after risk validation."""

    symbol: str
    decision: Decision
    volume: float


@dataclass
class ExecutionResult:
    """Result produced by the execution engine."""

    executed: bool
    reason: str


class ExecutionEngine:
    """AI_BRIDGE V2 execution engine."""

    def __init__(self) -> None:
        self._last_result = ExecutionResult(
            executed=False,
            reason="Engine not initialized.",
        )

    def execute(
        self,
        request: ExecutionRequest,
        risk: RiskEvaluation,
    ) -> ExecutionResult:
        """Execute a validated trading request."""

        if not risk.approved:
            self._last_result = ExecutionResult(
                executed=False,
                reason=risk.reason,
            )
            return self._last_result

        if request.volume <= 0.0:
            self._last_result = ExecutionResult(
                executed=False,
                reason="Invalid trade volume.",
            )
            return self._last_result

        if request.decision == Decision.HOLD:
            self._last_result = ExecutionResult(
                executed=False,
                reason="No execution required.",
            )
            return self._last_result

        self._last_result = ExecutionResult(
            executed=True,
            reason="Simulated execution completed.",
        )

        return self._last_result

    def last_result(self) -> ExecutionResult:
        """Return the last execution result."""

        return self._last_result

    def reset(self) -> None:
        """Reset the engine state."""

        self._last_result = ExecutionResult(
            executed=False,
            reason="Engine reset.",
        )
