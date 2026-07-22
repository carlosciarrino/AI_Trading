"""System inspector for AI_BRIDGE V2.

The system inspector provides a generic, read-only view of the
current system state, independent from the reporting functions
already available in the application layer.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass

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
