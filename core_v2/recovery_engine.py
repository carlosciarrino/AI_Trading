"""
Recovery engine for AI_BRIDGE V2.

The recovery engine evaluates the health status reported by the
monitoring engine and determines whether a recovery action is required.

This baseline implementation only reports the action that should be
taken. It does not perform any automatic recovery.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass

from core_v2.monitoring_engine import HealthReport


@dataclass(slots=True)
class RecoveryResult:
    """Result produced by the recovery engine."""

    recovery_required: bool
    action: str
    reason: str


class RecoveryEngine:
    """AI_BRIDGE V2 recovery engine."""

    def __init__(self) -> None:
        self._last_result = RecoveryResult(
            recovery_required=False,
            action="NONE",
            reason="Recovery engine not initialized.",
        )

    def evaluate(
        self,
        report: HealthReport,
    ) -> RecoveryResult:
        """Evaluate whether recovery is required."""

        if report.healthy:
            result = RecoveryResult(
                recovery_required=False,
                action="NONE",
                reason="System healthy.",
            )
        else:
            result = RecoveryResult(
                recovery_required=True,
                action="INVESTIGATE",
                reason=report.details,
            )

        self._last_result = result
        return result

    @property
    def last_result(self) -> RecoveryResult:
        """Return the last recovery evaluation."""

        return self._last_result
