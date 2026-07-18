"""
Event engine for AI_BRIDGE V2.

The event engine provides a simple event bus used by the AI_BRIDGE V2
pipeline.

This baseline implementation stores emitted events in memory and allows
them to be retrieved or cleared.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Event:
    """Single event emitted by the system."""

    name: str
    payload: dict[str, Any]


class EventEngine:
    """AI_BRIDGE V2 event engine."""

    def __init__(self) -> None:
        self._events: list[Event] = []

    def emit(self, event: Event) -> None:
        """Store a new event."""

        self._events.append(event)

    def events(self) -> list[Event]:
        """Return all recorded events."""

        return list(self._events)

    def clear(self) -> None:
        """Remove every stored event."""

        self._events.clear()

    @property
    def count(self) -> int:
        """Return the number of recorded events."""

        return len(self._events)
