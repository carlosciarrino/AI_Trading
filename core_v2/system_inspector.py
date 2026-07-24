"""System inspector for AI_BRIDGE V2.

The system inspector provides a generic, read-only view of the
current system state, independent from the reporting functions
already available in the application layer.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass

from core_v2.memory_engine import MemoryRecord, MemorySnapshot
from core_v2.orchestrator import OrchestratorStatistics
from core_v2.runtime_controller import RuntimeState
from core_v2.system_builder import AIComponents


@dataclass(slots=True)
class SystemSnapshot:
    """Generic snapshot of the current system state."""

    runtime_state: str
    cycle_count: int
    memory_records: int


class SystemInspector:
    """AI_BRIDGE V2 system inspector."""

    def __init__(self, components: AIComponents) -> None:
        self._components = components

    def snapshot(self) -> SystemSnapshot:
        """Return a snapshot of the current system state."""

        return SystemSnapshot(
            runtime_state=self._components.runtime.state.name,
            cycle_count=self._components.orchestrator.statistics.cycles,
            memory_records=self._components.memory.size,
        )

    def runtime_state(self) -> RuntimeState:
        """Return the current runtime state."""

        return self._components.runtime.state

    def memory_snapshot(self) -> MemorySnapshot:
        """Return the current memory snapshot."""

        return self._components.memory.snapshot()

    def last_pipeline_record(self) -> MemoryRecord | None:
        """Return the most recently stored memory record."""

        return self._components.memory.last_record()

    def recent_pipeline_records(
        self,
        limit: int = 10,
    ) -> list[MemoryRecord]:
        """Return the most recent pipeline records."""

        return self._components.memory.recent(limit)

    def orchestrator_statistics(self) -> OrchestratorStatistics:
        """Return the current orchestrator statistics."""

        return self._components.orchestrator.statistics
