"""Diagnostics interface for AI_BRIDGE V2.

This module is a thin command-line interface over the existing
application-level report functions. It contains no trading logic: it
only creates the application once and prints the requested reports.

Only the Python standard library is used.
"""

from __future__ import annotations

import argparse

from core_v2.application import (
    create_application,
    status_report,
    runtime_statistics,
    pipeline_summary,
    learning_summary,
    execution_summary,
    decision_history,
    system_report,
)


REPORTS = {
    "status": status_report,
    "runtime": runtime_statistics,
    "pipeline": pipeline_summary,
    "learning": learning_summary,
    "execution": execution_summary,
    "history": decision_history,
    "report": system_report,
}


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="AI_BRIDGE V2 diagnostics interface."
    )

    for name in REPORTS:
        parser.add_argument(
            f"--{name}",
            action="store_true",
            help=f"Print {name} report.",
        )

    return parser


def main() -> None:
    """Entry point for the diagnostics interface."""

    parser = build_parser()
    args = parser.parse_args()

    application = create_application()

    requested = [
        name for name in REPORTS if getattr(args, name)
    ]

    if not requested:
        print(system_report(application))
        return

    for name in requested:
        print(REPORTS[name](application))


if __name__ == "__main__":
    main()
