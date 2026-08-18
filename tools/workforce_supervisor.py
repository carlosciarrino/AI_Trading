#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "docs/workforce"
STATE = WF / "state.json"
EVIDENCE = WF / "evidence"

MAX_RETRIES = 3

@dataclass(frozen=True)
class Transition:
    stage: str
    next_stage: str

class WorkforceSupervisor:
    STAGES = (
        "RESEARCH",
        "ANALYSIS",
        "SECURITY",
        "ARCHITECTURE",
        "IMPLEMENTATION",
        "TEST",
        "REVIEW",
        "RELEASE",
    )

    def __init__(self, state_path: Path = STATE):
        self.state_path = state_path

    def load(self) -> dict:
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def save(self, state: dict) -> None:
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        tmp.replace(self.state_path)

    def transition(self, stage: str) -> str:
        if stage not in self.STAGES:
            raise ValueError(f"UNKNOWN_STAGE:{stage}")
        i = self.STAGES.index(stage)
        return self.STAGES[i + 1] if i + 1 < len(self.STAGES) else "RELEASED"

    def validate(self, state: dict) -> None:
        if state.get("human_required"):
            return
        stage = state.get("stage")
        if stage != "RELEASED" and stage not in self.STAGES:
            raise ValueError(f"INVALID_STATE:{stage}")
        retry = state.get("retry", 0)
        if not isinstance(retry, int) or retry < 0 or retry > MAX_RETRIES:
            raise ValueError("INVALID_RETRY_BOUND")

    def checkpoint(self, stage: str, ok: bool, output: str, proof: str) -> dict:
        state = self.load()
        if not ok:
            retry = int(state.get("retry", 0)) + 1
            state["retry"] = retry
            state["last_output"] = output
            state["last_proof"] = proof
            state["status"] = "RETRY" if retry < MAX_RETRIES else "HUMAN_REQUIRED"
            state["human_required"] = retry >= MAX_RETRIES
        else:
            state["retry"] = 0
            state["last_output"] = output
            state["last_proof"] = proof
            state.setdefault("completed", [])
            if stage not in state["completed"]:
                state["completed"].append(stage)
            nxt = self.transition(stage)
            state["stage"] = nxt
            state["status"] = "COMPLETED" if nxt == "RELEASED" else "RUNNING"
            state["human_required"] = False
        self.validate(state)
        self.save(state)
        return state
