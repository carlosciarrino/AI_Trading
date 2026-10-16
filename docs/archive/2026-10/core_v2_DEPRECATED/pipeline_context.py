"""Pipeline context for AI_BRIDGE V2.

This module defines the shared data container exchanged between
all engines during one orchestration cycle.

The context intentionally contains no business logic.
It is only responsible for transporting state between engines.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class PipelineContext:
    """Shared state exchanged between all engines."""

    cycle_id: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    # Market
    market_data: dict[str, Any] = field(default_factory=dict)

    # Decision
    decision: dict[str, Any] = field(default_factory=dict)

    # Risk
    risk: dict[str, Any] = field(default_factory=dict)

    # Execution
    order: dict[str, Any] = field(default_factory=dict)
    execution_result: dict[str, Any] = field(default_factory=dict)

    # Memory / Learning
    memory_data: dict[str, Any] = field(default_factory=dict)
    learning_data: dict[str, Any] = field(default_factory=dict)

    # Monitoring
    alerts: list[str] = field(default_factory=list)

    # Generic information
    metadata: dict[str, Any] = field(default_factory=dict)

    # Errors collected during the cycle
    errors: list[str] = field(default_factory=list)

    def reset(self, cycle_id: int) -> None:
        """Prepare the context for a new orchestration cycle."""

        self.cycle_id = cycle_id
        self.timestamp = datetime.utcnow()

        self.market_data.clear()
        self.decision.clear()
        self.risk.clear()
        self.order.clear()
        self.execution_result.clear()
        self.memory_data.clear()
        self.learning_data.clear()
        self.alerts.clear()
        self.metadata.clear()
        self.errors.clear()
