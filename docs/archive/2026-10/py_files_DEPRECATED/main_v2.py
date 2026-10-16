#!/usr/bin/env python3
"""Entry point for AI_BRIDGE V2.

Running this file (``python3 main_v2.py``) performs the AI_BRIDGE V2
bootstrap procedure defined in :mod:`core_v2.bootstrap` and reports the
outcome on standard output/error, with a process exit code suitable for
scripting (``0`` on success, ``1`` on any bootstrap failure).

This module contains no business logic of its own: it only invokes
:func:`core_v2.bootstrap.bootstrap` and translates its result (or its
exception) into console output and an exit code. It depends exclusively
on the Python standard library and on :mod:`core_v2.bootstrap`.
"""

from __future__ import annotations

import sys

from core_v2.bootstrap import BootstrapContext, bootstrap
from core_v2.exceptions import BootstrapError


def _report_success(context: BootstrapContext) -> None:
    """Log a final summary of a successful bootstrap.

    Args:
        context: The :class:`~core_v2.bootstrap.BootstrapContext`
            returned by a successful call to
            :func:`core_v2.bootstrap.bootstrap`.
    """
    context.logger.info(
        "AI_BRIDGE V2 is ready. Repository root: %s | Config sections: %s",
        context.repo_root,
        ", ".join(sorted(context.config.keys())),
    )


def main() -> int:
    """Run the AI_BRIDGE V2 bootstrap and report the outcome.

    Returns:
        ``0`` if the bootstrap completed successfully, ``1`` if it
        failed with a :class:`~core_v2.exceptions.BootstrapError`.
    """
    try:
        context = bootstrap()
    except BootstrapError as error:
        print(f"[AI_BRIDGE V2] Bootstrap failed: {error}", file=sys.stderr)
        return 1

    _report_success(context)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
