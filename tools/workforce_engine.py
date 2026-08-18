#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from workforce_workers import WORKERS

ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "docs/workforce"
STATE = WF / "state.json"
QUEUE = WF / "queue.json"
EVIDENCE = WF / "evidence"

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


def load(path: Path, default):
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def save(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )
    tmp.replace(path)


def evidence_path(stage: str) -> Path:
    index = STAGES.index(stage) + 1
    return EVIDENCE / f"{index:02d}_{stage.lower()}.log"


def evidence(stage: str, text: str):
    path = evidence_path(stage)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def previous_output(stage: str, state: dict) -> str:
    """
    Resolve previous stage output.

    Priority:
    1. state cache
    2. previous stage evidence
    """
    cached = state.get("last_output", "")
    if cached:
        return cached

    index = STAGES.index(stage)

    if index == 0:
        return ""

    previous_stage = STAGES[index - 1]
    path = evidence_path(previous_stage)

    if not path.exists():
        return ""

    try:
        text = path.read_text(encoding="utf-8").strip()
    except OSError:
        return ""

    if not text:
        return ""

    return text


def run_stage(
    stage: str,
    task: dict,
    previous: str,
) -> tuple[bool, str, str, str]:
    worker = WORKERS.get(stage)

    if worker is None:
        return False, "", "worker_missing", "HUMAN_REQUIRED"

    result = worker(task, previous)

    return (
        result.ok,
        result.output,
        result.evidence,
        result.next_action,
    )


def main() -> int:
    state = load(
        STATE,
        {
            "status": "RUNNING",
            "stage": "RESEARCH",
            "completed": [],
            "human_required": False,
            "last_output": "",
            "retry": 0,
        },
    )

    queue = load(QUEUE, {"tasks": []})

    task = next(
        (
            t
            for t in queue.get("tasks", [])
            if t.get("status") in {"READY", "RUNNING"}
        ),
        None,
    )

    if task is None:
        print("WORKFORCE: IDLE")
        return 0

    stage = state.get("stage", "RESEARCH")

    if stage == "RELEASED":
        state["status"] = "COMPLETED"
        task["status"] = "COMPLETED"
        save(STATE, state)
        save(QUEUE, queue)
        print("WORKFORCE: COMPLETED")
        return 0

    if stage not in STAGES:
        state["status"] = "HUMAN_REQUIRED"
        state["human_required"] = True
        save(STATE, state)
        print("WORKFORCE: HUMAN_REQUIRED")
        print(f"STAGE: {stage}")
        return 3

    previous = previous_output(stage, state)

    state["status"] = "RUNNING"
    state["human_required"] = False
    task["status"] = "RUNNING"

    ok, output, proof, next_action = run_stage(
        stage,
        task,
        previous,
    )

    evidence(
        stage,
        "\n".join(
            [
                f"NEXT_ACTION: {next_action}",
                proof,
                output,
            ]
        ),
    )

    if not ok:
        retries = state.get("retry", 0) + 1
        state["retry"] = retries

        if retries < 3:
            state["status"] = "RETRY"
            save(STATE, state)
            save(QUEUE, queue)
            print(f"STAGE: {stage} RETRY {retries}/3")
            return 2

        state["status"] = "HUMAN_REQUIRED"
        state["human_required"] = True
        save(STATE, state)
        save(QUEUE, queue)
        print("WORKFORCE: HUMAN_REQUIRED")
        print(f"STAGE: {stage}")
        print(f"REASON: {proof}")
        return 3

    state["last_output"] = output
    state["retry"] = 0

    if stage not in state.setdefault("completed", []):
        state["completed"].append(stage)

    index = STAGES.index(stage)

    if index + 1 < len(STAGES):
        next_stage = STAGES[index + 1]
        state["stage"] = next_stage
        state["status"] = "RUNNING"

        save(STATE, state)
        save(QUEUE, queue)

        print(f"STAGE: {stage} PASS -> {next_stage}")
        return 0

    state["stage"] = "RELEASED"
    state["status"] = "COMPLETED"
    task["status"] = "COMPLETED"

    save(STATE, state)
    save(QUEUE, queue)

    print("WORKFORCE: COMPLETED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
