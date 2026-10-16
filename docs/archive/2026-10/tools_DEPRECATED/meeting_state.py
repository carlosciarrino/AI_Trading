#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs/research/AGENT_REGISTRY.json"
BASELINE = ROOT / "sandbox/agent_lab/baseline"
STATE = ROOT / "docs/SESSION_STATE.md"


def run(*cmd: str) -> str:
    return subprocess.check_output(
        cmd,
        cwd=ROOT,
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()


def main() -> int:
    branch = run("git", "branch", "--show-current")
    head = run("git", "rev-parse", "--short", "HEAD")
    status = run("git", "status", "--short")

    registry_ok = REGISTRY.exists()
    agents = 0

    if registry_ok:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        agents = len(data.get("candidates", []))

    print("AI_BRIDGE V3 — MEETING STATE")
    print(f"branch={branch}")
    print(f"head={head}")
    print(f"working_tree={'CLEAN' if not status else 'DIRTY'}")
    print(f"baseline={'PASS' if (BASELINE / 'main_v2.py').exists() else 'FAIL'}")
    print(f"registry={'PASS' if registry_ok else 'FAIL'}")
    print(f"agents={agents}")

    if STATE.exists():
        lines = STATE.read_text(encoding="utf-8").splitlines()
        for line in lines:
            if line.startswith("- current:") or line.startswith("- next:"):
                print(line)

    if status:
        print("changes:")
        for line in status.splitlines()[:8]:
            print(f"  {line}")
        if len(status.splitlines()) > 8:
            print(f"  ... +{len(status.splitlines()) - 8}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
