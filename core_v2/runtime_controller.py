runtime_controller.py aperto
"""Runtime controller for AI_BRIDGE V2.

This module owns the runtime lifecycle state of AI_BRIDGE V2.

It provides a single RuntimeController class responsible for tracking
the current operating state of the application and validating state
transitions.

This module depends exclusively on the Python standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Final


class RuntimeState(Enum):
    """Possible runtime states."""

    BOOTSTRAP = "bootstrap"
    INITIALIZING = "initializing"
    RUNNING = "running"
    SAFE_MODE = "safe_mode"
    PAUSED = "paused"
    SHUTDOWN = "shutdown"


_ALLOWED_TRANSITIONS: Final[dict[RuntimeState, set[RuntimeState]]] = {
    RuntimeState.BOOTSTRAP: {
        RuntimeState.INITIALIZING,
    },
    RuntimeState.INITIALIZING: {
        RuntimeState.RUNNING,
        RuntimeState.SAFE_MODE,
        RuntimeState.SHUTDOWN,
    },
    RuntimeState.RUNNING: {
        RuntimeState.PAUSED,
        RuntimeState.SAFE_MODE,
        RuntimeState.SHUTDOWN,
    },
    RuntimeState.SAFE_MODE: {
        RuntimeState.RUNNING,
        RuntimeState.SHUTDOWN,
    },
    RuntimeState.PAUSED: {
        RuntimeState.RUNNING,
        RuntimeState.SHUTDOWN,
    },
    RuntimeState.SHUTDOWN: set(),
}


@dataclass(frozen=True)
class RuntimeSnapshot:
    """Immutable runtime snapshot."""

    state: RuntimeState
    started_at: datetime
    updated_at: datetime


class RuntimeController:
    """Controls the AI_BRIDGE runtime lifecycle."""

    def __init__(self) -> None:
        now = datetime.utcnow()
        self._state = RuntimeState.BOOTSTRAP
        self._started_at = now
        self._updated_at = now

    @property
    def state(self) -> RuntimeState:
        """Current runtime state."""
        return self._state

    @property
    def started_at(self) -> datetime:
        """Bootstrap timestamp."""
        return self._started_at

    @property
    def updated_at(self) -> datetime:
        """Last state change timestamp."""
        return self._updated_at

    def transition_to(self, new_state: RuntimeState) -> None:
        """Change runtime state.

        Raises:
            ValueError: if transition is not allowed.
        """
        if new_state == self._state:
            return

        allowed = _ALLOWED_TRANSITIONS[self._state]

        if new_state not in allowed:
            raise ValueError(
                f"Invalid runtime transition: "
                f"{self._state.value} -> {new_state.value}"
            )

        self._state = new_state
        self._updated_at = datetime.utcnow()

    def is_running(self) -> bool:
        """Return True if runtime is RUNNING."""
        return self._state is RuntimeState.RUNNING

    def is_safe_mode(self) -> bool:
        """Return True if runtime is SAFE_MODE."""
        return self._state is RuntimeState.SAFE_MODE

    def is_paused(self) -> bool:
        """Return True if runtime is PAUSED."""
        return self._state is RuntimeState.PAUSED

    def is_shutdown(self) -> bool:
        """Return True if runtime is SHUTDOWN."""
        return self._state is RuntimeState.SHUTDOWN

    def snapshot(self) -> RuntimeSnapshot:
        """Return an immutable snapshot."""
        return RuntimeSnapshot(
            state=self._state,
            started_at=self._started_at,
            updated_at=self._updated_at,
        )
