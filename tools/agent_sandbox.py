#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs/research/AGENT_REGISTRY.json"
BENCHMARK = ROOT / "tools/agent_sandbox_benchmark.py"
SUPERVISOR = ROOT / "tools/agent_supervisor.py"


def run(path: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0, result.stdout.strip()


def registry_summary() -> tuple[int, int]:
    if not REGISTRY.exists():
        return 0, 0

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    candidates = data.get("candidates", [])
    sandbox = sum(
        "sandbox" in c.get("capabilities", [])
        for c in candidates
    )
    return len(candidates), sandbox


def main() -> int:
    print("AI_BRIDGE V3 — AGENT SANDBOX")

    if not (ROOT / "sandbox/agent_lab/baseline").exists():
        print("BASELINE: FAIL")
        return 1

    print("BASELINE: PASS")

    ok_bench, _ = run(BENCHMARK)
    print(f"BENCHMARK: {'PASS' if ok_bench else 'FAIL'}")

    if not ok_bench:
        print("PROMOTION: BLOCKED")
        return 1

    ok_supervisor, _ = run(SUPERVISOR)
    print(f"SUPERVISOR: {'PASS' if ok_supervisor else 'FAIL'}")

    if not ok_supervisor:
        print("PROMOTION: BLOCKED")
        return 1

    total, sandbox = registry_summary()
    print(f"REGISTRY: {'PASS' if REGISTRY.exists() else 'FAIL'}")
    print(f"CANDIDATES: {total}")
    print(f"SANDBOX_CAPABLE: {sandbox}")
    print("PROMOTION: NOT PERFORMED")
    print("STATUS: READY_FOR_REVIEW")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
