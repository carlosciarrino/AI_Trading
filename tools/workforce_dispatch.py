#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class DispatchResult:
    ok: bool
    output: str
    evidence: str
    next_action: str

Worker = Callable[[dict, str], DispatchResult]

class WorkforceDispatcher:
    def __init__(self, workers: dict[str, Worker]):
        self.workers = dict(workers)

    def dispatch(self, stage: str, task: dict, previous: str) -> DispatchResult:
        worker = self.workers.get(stage)
        if worker is None:
            return DispatchResult(
                False, "", f"worker_missing:{stage}", "HUMAN_REQUIRED"
            )
        return worker(task, previous)
