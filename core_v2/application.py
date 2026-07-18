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
    """Create and initialize the AI_BRIDGE V2 application.

    The function performs:
    1. Environment bootstrap.
    2. Engine construction.
    3. Component wiring.

    Returns:
        A fully initialized application context.
    """

    bootstrap_context = bootstrap()

    components = build_system(
        configuration=bootstrap_context.config
    )

    components.orchestrator.start()

    return ApplicationContext(
        bootstrap=bootstrap_context,
        components=components,
    )
