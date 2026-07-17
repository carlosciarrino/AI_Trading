"""Execution engine for AI_BRIDGE V2.

This module provides the execution stage of the AI_BRIDGE V2 pipeline.

The execution engine is responsible for transforming an approved trading
decision into an execution result. In the Baseline 1.0 implementation,
execution is simulated only: no broker, network connection or external
platform is contacted.

The module depends exclusively on the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class ExecutionStatus(Enum):
    """Possible execution outcomes."""

    SUCCESS = "SUCCESS"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


@dataclass(slots=True)
class ExecutionRequest:
    """Request received by the execution engine."""

    symbol: str
    action: str
    volume: float


@dataclass(slots=True)
class ExecutionResult:
    """Result returned by the execution engine."""

    status: ExecutionStatus
    symbol: str
    action: str
    volume: float
    message: str


class ExecutionBackend(Protocol):
    """Protocol implemented by every execution backend."""

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        """Execute a trading request."""


class SimulatedExecutionBackend:
    """Simple simulated execution backend."""

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        """Simulate a successful execution."""

        return ExecutionResult(
            status=ExecutionStatus.SUCCESS,
            symbol=request.symbol,
            action=request.action,
            volume=request.volume,
            message="Simulated execution completed successfully.",
        )


class ExecutionEngine:
    """Execution engine for AI_BRIDGE V2."""

    def __init__(
        self,
        backend: ExecutionBackend | None = None,
    ) -> None:
        """Create a new execution engine."""

        if backend is None:
            backend = SimulatedExecutionBackend()

        self._backend = backend

    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        """Execute a trading request."""

        return self._backend.execute(request)
