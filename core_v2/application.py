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


def pipeline_summary(application: ApplicationContext) -> str:
    """Return a simple textual summary of the last pipeline cycle."""

    record = application.components.memory.last_record()

    if record is None:
        return "No pipeline executed."

    decision = record.data["decision"]["decision"]
    risk_approved = record.data["risk"]["approved"]
    risk_reason = record.data["risk"]["reason"]
    execution_result = record.data["execution_result"]

    risk = "APPROVED" if risk_approved else "REJECTED"

    executed = bool(execution_result and execution_result.get("executed"))
    execution = "EXECUTED" if executed else "NOT EXECUTED"

    lines = [
        "=" * 30,
        " LAST PIPELINE",
        "=" * 30,
        f"{'Decision':<9}: {decision}",
        f"{'Risk':<9}: {risk}",
        f"{'Execution':<9}: {execution}",
        f"{'Reason':<9}: {risk_reason}",
        f"{'Memory':<9}: {application.components.memory.size} records",
    ]

    return "\n".join(lines)


def decision_history(application: ApplicationContext, limit: int = 10) -> str:
    """Return a simple textual history of recent decisions."""

    records = application.components.memory.recent(limit)

    if not records:
        return "No decision history available."

    lines = [
        "=" * 30,
        " DECISION HISTORY",
        "=" * 30,
    ]

    for index, record in enumerate(records, start=1):
        lines.append(
            f"#{index} {record.data['decision']['decision']}"
        )

    return "\n".join(lines)


def runtime_statistics(application: ApplicationContext) -> str:
    """Return a simple textual runtime statistics report."""

    runtime = application.components.runtime
    orchestrator = application.components.orchestrator
    memory = application.components.memory

    record = memory.last_record()
    last_decision = (
        record.data["decision"]["decision"] if record else "NONE"
    )

    lines = [
        "=" * 49,
        " AI_BRIDGE V2 RUNTIME STATISTICS",
        "=" * 49,
        f"{'Runtime':.<19} {runtime.state.name}",
        f"{'Cycles':.<19} {orchestrator.statistics.cycles}",
        f"{'Memory Records':.<19} {memory.size}",
        f"{'Last Decision':.<19} {last_decision}",
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


def learning_summary(application: ApplicationContext) -> str:
    """Return a simple textual learning summary."""

    records = application.components.memory.records()

    application.components.learning.analyse_records(records)
    decision_counts = application.components.learning.analyse_decisions(records)

    report = application.components.learning.analyse(len(records))
    recommendation = report.recommendations[0]

    lines = [
        "=" * 33,
        " LEARNING SUMMARY",
        "=" * 33,
        f"{'Samples':.<20} {report.samples}",
        f"{'BUY':.<20} {decision_counts.get('BUY', 0)}",
        f"{'SELL':.<20} {decision_counts.get('SELL', 0)}",
        f"{'HOLD':.<20} {decision_counts.get('HOLD', 0)}",
        f"{'Recommendation':.<20} {recommendation}",
    ]

    return "\n".join(lines)


def execution_summary(application: ApplicationContext) -> str:
    """Return a simple textual execution summary."""

    records = application.components.memory.records()

    counts = application.components.learning.analyse_execution_results(records)

    lines = [
        "=" * 33,
        " EXECUTION SUMMARY",
        "=" * 33,
        f"{'Approved':.<19} {counts['approved']}",
        f"{'Rejected':.<19} {counts['rejected']}",
        f"{'Executed':.<19} {counts['executed']}",
        f"{'Not Executed':.<19} {counts['not_executed']}",
    ]

    return "\n".join(lines)
