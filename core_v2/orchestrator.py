"""System orchestrator for AI_BRIDGE V2.

The orchestrator coordinates the execution lifecycle of AI_BRIDGE V2.

At this stage it does not execute trading logic directly. Instead, it
provides the central coordination point that future engines
(market, decision, risk, execution, monitoring, learning, recovery,
memory) will register with.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from core_v2.runtime_controller import RuntimeController, RuntimeState


EngineCallback = Callable[[], None]


@dataclass
class EngineRegistry:
    """Registry containing the callbacks of every engine."""

    market: EngineCallback | None = None
    decision: EngineCallback | None = None
    risk: EngineCallback | None = None
    execution: EngineCallback | None = None
    monitoring: EngineCallback | None = None
    recovery: EngineCallback | None = None
    learning: EngineCallback | None = None
    memory: EngineCallback | None = None


@dataclass
class OrchestratorStatistics:
    """Runtime statistics."""

    cycles: int = 0
    executed_callbacks: int = 0


@dataclass
class Orchestrator:
    """Coordinates all AI_BRIDGE V2 engines."""

    runtime: RuntimeController
    registry: EngineRegistry = field(default_factory=EngineRegistry)
    statistics: OrchestratorStatistics = field(
        default_factory=OrchestratorStatistics
    )

    def register_market(self, callback: EngineCallback) -> None:
        self.registry.market = callback

    def register_decision(self, callback: EngineCallback) -> None:
        self.registry.decision = callback

    def register_risk(self, callback: EngineCallback) -> None:
        self.registry.risk = callback

    def register_execution(self, callback: EngineCallback) -> None:
        self.registry.execution = callback

    def register_monitoring(self, callback: EngineCallback) -> None:
        self.registry.monitoring = callback

    def register_recovery(self, callback: EngineCallback) -> None:
        self.registry.recovery = callback

    def register_learning(self, callback: EngineCallback) -> None:
        self.registry.learning = callback

    def register_memory(self, callback: EngineCallback) -> None:
        self.registry.memory = callback

    def start(self) -> None:
        """Move runtime into RUNNING state."""

        if self.runtime.state is RuntimeState.BOOTSTRAP:
            self.runtime.transition_to(RuntimeState.INITIALIZING)

        if self.runtime.state is RuntimeState.INITIALIZING:
            self.runtime.transition_to(RuntimeState.RUNNING)

    def stop(self) -> None:
        """Shutdown runtime."""

        if self.runtime.state is not RuntimeState.SHUTDOWN:
            self.runtime.transition_to(RuntimeState.SHUTDOWN)

    def run_cycle(self) -> None:
        """Execute one orchestration cycle."""

        if not self.runtime.is_running():
            return

        callbacks = (
            self.registry.market,
            self.registry.decision,
            self.registry.risk,
            self.registry.execution,
            self.registry.monitoring,
            self.registry.learning,
            self.registry.memory,
            self.registry.recovery,
        )

        for callback in callbacks:
            if callback is None:
                continue

            callback()
            self.statistics.executed_callbacks += 1

        self.statistics.cycles += 1
