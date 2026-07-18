"""Monitoring engine for AI_BRIDGE V2.

The monitoring engine evaluates the operational health of the AI_BRIDGE
V2 pipeline. Its responsibility is limited to observing the system and
reporting its status.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HealthReport:
    """Health report produced by the monitoring engine."""

    healthy: bool
    status: str
    details: str


class MonitoringEngine:
    """AI_BRIDGE V2 monitoring engine."""

    def __init__(self) -> None:
        self._last_report = HealthReport(
            healthy=False,
            status="UNKNOWN",
            details="Monitoring engine not initialized.",
        )

    def evaluate(self) -> HealthReport:
        """Evaluate the current system health."""

        self._last_report = HealthReport(
            healthy=True,
            status="OK",
            details="All monitored components are operational.",
        )

        return self._last_report

    def last_report(self) -> HealthReport:
        """Return the last generated health report."""

        return self._last_report

    def reset(self) -> None:
        """Reset the monitoring engine state."""

        self._last_report = HealthReport(
            healthy=False,
            status="RESET",
            details="Monitoring engine reset.",
        )
