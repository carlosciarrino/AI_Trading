#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "docs/workforce/state.json"
QUEUE = ROOT / "docs/workforce/queue.json"
CONTRACT = ROOT / "docs/workforce/OPERATING_CONTRACT.md"

def load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def run(cmd):
    return subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

def main():
    if not CONTRACT.exists():
        print("WORKFORCE_CONTRACT: FAIL")
        return 3

    state = load(STATE, {})
    queue = load(QUEUE, {"tasks": []})

    print("AI_BRIDGE V3 — WORKFORCE BOOTSTRAP")
    print("CONTRACT: PASS")
    print(f"STATE: {state.get('status', 'MISSING')}")
    print(f"STAGE: {state.get('stage', 'MISSING')}")
    print(f"HUMAN_REQUIRED: {state.get('human_required', False)}")
    print(f"QUEUE_TASKS: {len(queue.get('tasks', []))}")

    engine = ROOT / "tools/workforce_engine.py"
    if not engine.exists():
        print("ENGINE: MISSING")
        return 3

    print("ENGINE: PASS")
    print("POLICY: BINDING")
    print("HUMAN: ONLY_IF_REQUIRED")
    print("COPY_PASTE: AGGREGATED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
