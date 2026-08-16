"""System orchestrator for AI_BRIDGE V2.

The orchestrator coordinates the execution lifecycle of AI_BRIDGE V2.

This module maintains backward compatibility with the callback registry
system while introducing direct engine orchestration through the
AIComponents container.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Any

from core_v2.runtime_controller import RuntimeController, RuntimeState
from core_v2.pipeline_context import PipelineContext
from core_v2.execution_engine import ExecutionRequest
from core_v2.memory_engine import MemoryRecord


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
    """Coordinates all AI_BRIDGE V2 engines.

    The callback registry remains active during the migration phase.
    Direct orchestration is performed through the AIComponents container.
    """

    runtime: RuntimeController

    components: Any | None = None

    registry: EngineRegistry = field(
        default_factory=EngineRegistry
    )

    statistics: OrchestratorStatistics = field(
        default_factory=OrchestratorStatistics
    )

    def attach_components(self, components: Any) -> None:
        """Attach AIComponents container."""

        self.components = components

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
            self.runtime.transition_to(
                RuntimeState.INITIALIZING
            )

        if self.runtime.state is RuntimeState.INITIALIZING:
            self.runtime.transition_to(
                RuntimeState.RUNNING
            )

    def stop(self) -> None:
        """Shutdown runtime."""

        if self.runtime.state is not RuntimeState.SHUTDOWN:
            self.runtime.transition_to(
                RuntimeState.SHUTDOWN
            )

    def run_pipeline_cycle(self) -> PipelineContext:
        """Execute one complete AI_BRIDGE V2 engine pipeline."""

        context = PipelineContext(
            cycle_id=self.statistics.cycles + 1
        )

        if not self.runtime.is_running():
            context.errors.append(
                "Runtime is not running."
            )
            return context

        if self.components is None:
            context.errors.append(
                "AIComponents container not attached."
            )
            return context

        try:
            self.components.market.update()

            context.market_data = {
                "symbols": self.components.market.get_symbols(),
                "ready": self.components.market.is_ready(),
            }

            decision_result = (
                self.components.decision.evaluate()
            )

            context.decision = {
                "decision": decision_result.decision.value,
                "confidence": decision_result.confidence,
                "reason": decision_result.reason,
            }

            risk_result = (
                self.components.risk.evaluate(
                    decision_result
                )
            )

            context.risk = {
                "approved": risk_result.approved,
                "reason": risk_result.reason,
            }

            symbols = self.components.market.get_symbols()

            if symbols:
                request = ExecutionRequest(
                    symbol=symbols[0],
                    decision=decision_result.decision,
                    volume=1.0,
                )

                execution_result = (
                    self.components.execution.execute(
                        request,
                        risk_result,
                    )
                )

                context.order = {
                    "symbol": request.symbol,
                    "volume": request.volume,
                    "decision": request.decision.value,
                }

                context.execution_result = {
                    "executed": execution_result.executed,
                    "reason": execution_result.reason,
                }

            health = (
                self.components.monitoring.evaluate()
            )

            context.metadata["health"] = str(
                health
            )

            recovery = (
                self.components.recovery.evaluate(
                    health
                )
            )

            context.metadata["recovery"] = str(
                recovery
            )

            memory_record = MemoryRecord(
                category="pipeline_cycle",
                data={
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "decision": context.decision,
                    "risk": context.risk,
                    "execution_result": context.execution_result,
                },
            )

            self.components.memory.store(memory_record)

            context.memory_data = {
                "records": self.components.memory.size
            }

            self.components.learning.analyse(
                self.components.memory.size
            )

            context.learning_data = {
                "samples": self.components.memory.size
            }

        except Exception as error:
            context.errors.append(
                str(error)
            )

        self.statistics.cycles += 1

        return context

    def run_cycle(self) -> None:
        """Execute one orchestration cycle using callbacks."""

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
