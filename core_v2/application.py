"""Application layer for AI_BRIDGE V2.

This module connects the bootstrap environment with the AI_BRIDGE V2
runtime system.

The application layer is responsible for:
- running bootstrap;
- creating the engine container;
- preparing the runtime;
- returning the initialized AIComponents.

It does not contain trading logic.

Only the Python standard library is used.
"""

from __future__ import annotations

from dataclasses import dataclass

from core_v2.bootstrap import BootstrapContext, bootstrap
from core_v2.system_builder import AIComponents, build_system


@dataclass
class ApplicationContext:
    """Runtime context of the AI_BRIDGE V2 application."""

    bootstrap: BootstrapContext
    components: AIComponents


def create_application() -> ApplicationContext:
    """Create and initialize the AI_BRIDGE V2 application."""

    bootstrap_context = bootstrap()

    components = build_system(
        configuration=bootstrap_context.config
    )

    components.orchestrator.start()

    return ApplicationContext(
        bootstrap=bootstrap_context,
        components=components,
    )


def status_report(application: ApplicationContext) -> str:
    """Return a simple textual status report."""

    runtime = application.components.runtime
    orchestrator = application.components.orchestrator
    memory = application.components.memory

    lines = [
        "=" * 49,
        " AI_BRIDGE V2 STATUS REPORT",
        "=" * 49,
        "",
        f"Runtime............ {runtime.state.name}",
        f"Cycles............. {orchestrator.statistics.cycles}",
        f"Memory Records..... {memory.size}",
        "",
        "=" * 49,
    ]

    return "\n".join(lines)


def cycle_history(application: ApplicationContext, limit: int = 5) -> str:
    """Return a simple textual history of the most recent cycles."""

    records = application.components.memory.recent(limit)

    if not records:
        return "No cycle history available."

    lines = ["Last cycles"]

    for index, record in enumerate(records, start=1):
        lines.append(
            f"#{index} {record.data['decision']['decision']}"
        )

    return "\n".join(lines)
