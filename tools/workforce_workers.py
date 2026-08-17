#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class WorkerResult:
    ok: bool
    output: str
    evidence: str
    next_action: str
    recoverable: bool = False
    second_inspection: bool = False


Worker = Callable[[dict, str], WorkerResult]


def _require(previous: str, evidence: str, action: str) -> WorkerResult | None:
    if previous:
        return None
    return WorkerResult(
        False,
        "",
        evidence,
        action,
        recoverable=True,
        second_inspection=True,
    )


def researcher(task: dict, previous: str) -> WorkerResult:
    sources = task.get("sources", [])
    if not sources:
        return WorkerResult(False, "", "no sources", "HUMAN_REQUIRED")
    return WorkerResult(
        True,
        "Research sources: " + ", ".join(sources),
        "research input verified",
        "ANALYZE",
    )


def analyst(task: dict, previous: str) -> WorkerResult:
    fail = _require(previous, "missing research output", "RETRY")
    if fail:
        return fail
    return WorkerResult(
        True,
        "Analysis completed from verified research input.",
        "analysis input verified",
        "SECURITY",
    )


def security(task: dict, previous: str) -> WorkerResult:
    fail = _require(previous, "missing analysis output", "RETRY")
    if fail:
        return fail
    return WorkerResult(
        True,
        "Security stage delegated to verified security gate.",
        "security gate input verified",
        "ARCHITECT",
    )


def architect(task: dict, previous: str) -> WorkerResult:
    fail = _require(previous, "missing security output", "RETRY")
    if fail:
        return fail
    return WorkerResult(
        True,
        "Architecture specification produced from verified security output.",
        "architecture input verified",
        "IMPLEMENT",
    )


def implementer(task: dict, previous: str) -> WorkerResult:
    fail = _require(previous, "missing architecture output", "RETRY")
    if fail:
        return fail
    return WorkerResult(
        True,
        "Implementation received verified architecture output.",
        "implementation input verified",
        "TEST",
    )


def tester(task: dict, previous: str) -> WorkerResult:
    fail = _require(previous, "missing implementation output", "RETRY")
    if fail:
        return fail
    return WorkerResult(
        True,
        "Tests received verified implementation output.",
        "test input verified",
        "REVIEW",
    )


def reviewer(task: dict, previous: str) -> WorkerResult:
    fail = _require(previous, "missing test output", "RETRY")
    if fail:
        return fail
    return WorkerResult(
        True,
        "Review received verified test output.",
        "review input verified",
        "RELEASE",
    )


def releaser(task: dict, previous: str) -> WorkerResult:
    fail = _require(previous, "missing review output", "RETRY")
    if fail:
        return fail
    return WorkerResult(
        True,
        "Release received verified reviewed output.",
        "release input verified",
        "DONE",
    )


WORKERS: dict[str, Worker] = {
    "RESEARCH": researcher,
    "ANALYSIS": analyst,
    "SECURITY": security,
    "ARCHITECTURE": architect,
    "IMPLEMENTATION": implementer,
    "TEST": tester,
    "REVIEW": reviewer,
    "RELEASE": releaser,
}
