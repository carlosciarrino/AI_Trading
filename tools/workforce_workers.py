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

Worker = Callable[[dict, str], WorkerResult]

def researcher(task, previous):
    sources = task.get("sources", [])
    if not sources:
        return WorkerResult(False, "", "no sources", "HUMAN_REQUIRED")
    return WorkerResult(
        True,
        "Research sources: " + ", ".join(sources),
        "research sources registered",
        "ANALYZE",
    )

def analyst(task, previous):
    if not previous:
        return WorkerResult(False, "", "missing research output", "RETRY")
    return WorkerResult(
        True,
        "Analysis completed from verified research input.",
        "analysis input received",
        "SECURITY",
    )

def security(task, previous):
    if not previous:
        return WorkerResult(False, "", "missing analysis output", "RETRY")
    return WorkerResult(
        True,
        "Security review requires existing security gate.",
        "security gate required",
        "ARCHITECT",
    )

def architect(task, previous):
    if not previous:
        return WorkerResult(False, "", "missing security output", "RETRY")
    return WorkerResult(
        True,
        "Architecture specification produced.",
        "architecture input verified",
        "IMPLEMENT",
    )

def implementer(task, previous):
    if not previous:
        return WorkerResult(False, "", "missing architecture output", "RETRY")
    return WorkerResult(
        True,
        "Implementation stage received architecture output.",
        "implementation input verified",
        "TEST",
    )

def tester(task, previous):
    if not previous:
        return WorkerResult(False, "", "missing implementation output", "RETRY")
    return WorkerResult(
        True,
        "Test stage received implementation output.",
        "test input verified",
        "REVIEW",
    )

def reviewer(task, previous):
    if not previous:
        return WorkerResult(False, "", "missing test output", "RETRY")
    return WorkerResult(
        True,
        "Review stage received test output.",
        "review input verified",
        "RELEASE",
    )

def releaser(task, previous):
    if not previous:
        return WorkerResult(False, "", "missing review output", "RETRY")
    return WorkerResult(
        True,
        "Release stage received reviewed output.",
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
