#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "docs/workforce/state.json"
ENGINE = ROOT / "tools/workforce_engine.py"
EVIDENCE = ROOT / "docs/workforce/evidence"
MAX_ATTEMPTS = 32
TERMINAL = {"COMPLETED", "HUMAN_REQUIRED"}

def read_state():
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "HUMAN_REQUIRED",
                "human_required": True,
                "last_output": "",
                "error": f"STATE_READ_ERROR: {exc}"}

def run():
    if not ENGINE.exists():
        print("WORKFORCE: HUMAN_REQUIRED")
        print("REASON: ENGINE_MISSING")
        return 3

    EVIDENCE.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        before = read_state()
        before_stage = before.get("stage")
        before_cycle = before.get("cycle")

        proc = subprocess.run(
            [sys.executable, str(ENGINE)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

        output = (proc.stdout or "") + (proc.stderr or "")
        print(output, end="")

        after = read_state()
        status = after.get("status")
        stage = after.get("stage")

        evidence = EVIDENCE / "workforce_run.log"
        with evidence.open("a", encoding="utf-8") as f:
            f.write(
                f"\n=== RUN {attempt} ===\n"
                f"BEFORE_STATUS={before.get('status')}\n"
                f"BEFORE_STAGE={before_stage}\n"
                f"BEFORE_CYCLE={before_cycle}\n"
                f"RETURN_CODE={proc.returncode}\n"
                f"OUTPUT={output}\n"
                f"AFTER_STATUS={status}\n"
                f"AFTER_STAGE={stage}\n"
            )

        if status == "COMPLETED":
            print("WORKFORCE_RUN: COMPLETED")
            print(f"ATTEMPTS: {attempt}")
            return 0

        if status == "READY" and stage == "NEXT_TASK":
            print("WORKFORCE_RUN: READY")
            print(f"ATTEMPTS: {attempt}")
            return 0

        if status == "READY" and not after.get("human_required", False):
            print("WORKFORCE_RUN: IDLE")
            print(f"ATTEMPTS: {attempt}")
            return 0

        if status == "HUMAN_REQUIRED" or after.get("human_required") is True:
            print("WORKFORCE_RUN: HUMAN_REQUIRED")
            print(f"STAGE: {stage}")
            print(f"ATTEMPTS: {attempt}")
            return 3

        progressed = (
            stage != before_stage
            or after.get("cycle") != before_cycle
            or status in {"RUNNING", "RETRY"}
        )

        if proc.returncode not in {0, 2} and not progressed:
            print("WORKFORCE_RUN: HUMAN_REQUIRED")
            print("REASON: UNRECOVERED_ENGINE_FAILURE")
            print(f"STAGE: {stage}")
            print(f"ATTEMPTS: {attempt}")
            return 3

    print("WORKFORCE_RUN: HUMAN_REQUIRED")
    print("REASON: RETRY_LIMIT")
    print(f"MAX_ATTEMPTS: {MAX_ATTEMPTS}")
    return 3

if __name__ == "__main__":
    raise SystemExit(run())
