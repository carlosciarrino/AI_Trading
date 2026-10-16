"""System diagnostics for AI_BRIDGE V2.

This module centralizes access to runtime diagnostic information.

It contains no presentation logic and uses SystemInspector as the
single source of diagnostic data.

Only the Python standard library is used.
"""

from __future__ import annotations

from core_v2.memory_engine import MemoryRecord, MemorySnapshot
from core_v2.orchestrator import OrchestratorStatistics
from core_v2.runtime_controller import RuntimeSnapshot
from core_v2.system_builder import AIComponents
from core_v2.system_inspector import (
    SystemInspector,
    SystemSnapshot,
)


class SystemDiagnostics:
    """Central diagnostic access layer."""

    def __init__(self, components: AIComponents) -> None:
        self._inspector = SystemInspector(
            components
        )

    def snapshot(self) -> SystemSnapshot:
        """Return the current system snapshot."""

        return self._inspector.snapshot()

    def runtime(self) -> RuntimeSnapshot:
        """Return the current runtime snapshot."""

        return self._inspector.runtime_state().snapshot()

    def memory(self) -> MemorySnapshot:
        """Return the current memory snapshot."""

        return self._inspector.memory_snapshot()

    def orchestrator(
        self,
    ) -> OrchestratorStatistics:
        """Return orchestrator statistics."""

        return self._inspector.orchestrator_statistics()

    def last_pipeline(
        self,
    ) -> MemoryRecord | None:
        """Return the latest pipeline record."""

        return self._inspector.last_pipeline_record()
    def recent_pipeline(
        self,
        limit: int = 10,
    ) -> list[MemoryRecord]:
        """Return recent pipeline records."""

        return self._inspector.recent_pipeline_records(
            limit
        )
