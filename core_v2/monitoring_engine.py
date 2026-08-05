"""Monitoring engine for AI_BRIDGE V2.

The monitoring engine evaluates the operational health of the AI_BRIDGE
V2 pipeline.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class HealthReport:
    """Health report produced by the monitoring engine."""

    healthy: bool
    status: str
    details: str

    runtime_state: str = "UNKNOWN"
    memory_records: int = 0
    pipeline_cycles: int = 0
    alerts: list[str] = field(default_factory=list)


class MonitoringEngine:
    """AI_BRIDGE V2 monitoring engine."""

    def __init__(self) -> None:
        self._components: Any | None = None

        self._last_report = HealthReport(
            healthy=False,
            status="UNKNOWN",
            details="Monitoring engine not initialized.",
        )

    def attach_components(self, components: Any) -> None:
        """Attach AIComponents after system construction."""

        self._components = components

    def evaluate(self) -> HealthReport:
        """Evaluate current system health."""

        if self._components is None:
            self._last_report = HealthReport(
                healthy=False,
                status="DISCONNECTED",
                details="AIComponents not attached.",
                alerts=["components_not_attached"],
            )
            return self._last_report

        runtime = self._components.runtime.state.name
        memory = self._components.memory.size
        cycles = self._components.orchestrator.statistics.cycles

        alerts: list[str] = []

        if runtime != "RUNNING":
            alerts.append("runtime_not_running")

        healthy = not alerts

        self._last_report = HealthReport(
            healthy=healthy,
            status="OK" if healthy else "WARNING",
            details=(
                "All monitored components are operational."
                if healthy
                else "Monitoring detected one or more issues."
            ),
            runtime_state=runtime,
            memory_records=memory,
            pipeline_cycles=cycles,
            alerts=alerts,
        )

        return self._last_report

    def last_report(self) -> HealthReport:
        """Return last health report."""

        return self._last_report

    def reset(self) -> None:
        """Reset monitoring state."""

        self._last_report = HealthReport(
            healthy=False,
            status="RESET",
            details="Monitoring engine reset.",
        )
