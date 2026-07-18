"""System builder for AI_BRIDGE V2.

This module creates and connects the AI_BRIDGE V2 components.

The system builder is responsible only for composition:
creating engines and wiring their dependencies.

It does not contain trading logic.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core_v2.market_engine import MarketEngine
from core_v2.decision_engine import DecisionEngine
from core_v2.risk_engine import RiskEngine, RiskLimits
from core_v2.execution_engine import ExecutionEngine
from core_v2.monitoring_engine import MonitoringEngine
from core_v2.recovery_engine import RecoveryEngine
from core_v2.memory_engine import MemoryEngine
from core_v2.learning_engine import LearningEngine
from core_v2.event_engine import EventEngine
from core_v2.runtime_controller import RuntimeController
from core_v2.orchestrator import Orchestrator


@dataclass
class AIComponents:
    """Container holding all AI_BRIDGE V2 components.

    This class is the official container of all system engines.

    It keeps engine references centralized and provides
    a simple access layer for future orchestration,
    pipeline execution and engine communication.
    """

    runtime: RuntimeController
    orchestrator: Orchestrator

    market: MarketEngine
    decision: DecisionEngine
    risk: RiskEngine
    execution: ExecutionEngine
    monitoring: MonitoringEngine
    recovery: RecoveryEngine
    memory: MemoryEngine
    learning: LearningEngine
    events: EventEngine

    _registry: dict[str, Any] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        """Build internal engine registry."""

        self._registry = {
            "market": self.market,
            "decision": self.decision,
            "risk": self.risk,
            "execution": self.execution,
            "monitoring": self.monitoring,
            "recovery": self.recovery,
            "memory": self.memory,
            "learning": self.learning,
            "events": self.events,
        }

    def get_engine(self, name: str) -> Any | None:
        """Return an engine by name."""

        return self._registry.get(name)

    def has_engine(self, name: str) -> bool:
        """Check whether an engine exists."""

        return name in self._registry

    def engines(self) -> dict[str, Any]:
        """Return all registered engines."""

        return dict(self._registry)


def build_system(
    configuration: dict[str, dict[str, str]],
) -> AIComponents:
    """Create and connect the AI_BRIDGE V2 system.

    The builder creates all engines and connects them.
    It does not execute the system lifecycle.
    """

    runtime = RuntimeController()

    market = MarketEngine(
        configuration=configuration.get("market", {})
    )

    market.initialize()

    decision = DecisionEngine(
        market_engine=market
    )

    risk = RiskEngine(
        limits=RiskLimits(
            max_risk_per_trade=1.0,
            max_daily_loss=5.0,
            max_open_positions=3,
        )
    )

    execution = ExecutionEngine()

    monitoring = MonitoringEngine()

    recovery = RecoveryEngine()

    memory = MemoryEngine()

    learning = LearningEngine()

    events = EventEngine()

    orchestrator = Orchestrator(
        runtime=runtime
    )

    # ==========================================================
    # Temporary compatibility layer
    #
    # The orchestrator still uses callbacks.
    # This will be replaced in a later migration step
    # with direct engine orchestration.
    # ==========================================================

    orchestrator.register_market(
        market.update
    )

    orchestrator.register_decision(
        decision.evaluate
    )

    orchestrator.register_monitoring(
        monitoring.evaluate
    )

    orchestrator.register_recovery(
        lambda: recovery.evaluate(
            monitoring.last_report()
        )
    )

    orchestrator.register_learning(
        lambda: learning.analyse(
            memory.size
        )
    )

    orchestrator.register_memory(
        lambda: memory.snapshot()
    )

    return AIComponents(
        runtime=runtime,
        orchestrator=orchestrator,
        market=market,
        decision=decision,
        risk=risk,
        execution=execution,
        monitoring=monitoring,
        recovery=recovery,
        memory=memory,
        learning=learning,
        events=events,
    )
