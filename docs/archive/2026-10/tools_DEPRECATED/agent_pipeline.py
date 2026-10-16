#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs/research/AGENT_REGISTRY.json"
SECURITY = ROOT / "tools/agent_security.py"
BENCHMARK = ROOT / "tools/agent_sandbox_benchmark.py"


def run(cmd: list[str]) -> tuple[bool, str]:
    r = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return r.returncode == 0, r.stdout.strip()


def main() -> int:
    print("AI_BRIDGE V3 — AGENT PIPELINE")

    if not REGISTRY.exists():
        print("REGISTRY: FAIL")
        print("DECISION: BLOCKED")
        return 1

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    candidates = [
        c for c in data.get("candidates", [])
        if "sandbox" in c.get("capabilities", [])
        and c.get("status") == "RESEARCH_ONLY"
    ]

    print(f"CANDIDATES: {len(candidates)}")

    if not candidates:
        print("DECISION: BLOCKED")
        return 1

    for candidate in candidates:
        name = candidate["name"]
        path = ROOT / candidate["repository"]

        if not path.is_dir():
            print(f"{name}: PATH_FAIL")
            print("DECISION: BLOCKED")
            return 1

        ok, output = run([
            sys.executable,
            str(SECURITY),
            str(path),
        ])

        if not ok:
            print(f"{name}: SECURITY_FAIL")
            print("DECISION: REJECT")
            return 1

        print(f"{name}: SECURITY_PASS")

    ok, _ = run([sys.executable, str(BENCHMARK)])

    print(f"BENCHMARK: {'PASS' if ok else 'FAIL'}")

    if not ok:
        print("DECISION: REJECT")
        return 1

    print("BASELINE: PROTECTED")
    print("PROMOTION: NOT PERFORMED")
    print("DECISION: READY_FOR_OWNER")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
