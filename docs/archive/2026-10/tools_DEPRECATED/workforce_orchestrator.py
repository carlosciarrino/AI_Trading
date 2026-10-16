#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REGISTRY = ROOT / "docs/research/AGENT_REGISTRY.json"

DISCOVERY = ROOT / "tools/candidate_discovery.py"
SECURITY = ROOT / "tools/agent_security.py"
SANDBOX = ROOT / "tools/agent_sandbox.py"
ASSIGNMENT = ROOT / "tools/candidate_assignment.py"
SCHEDULER = ROOT / "tools/workforce_scheduler.py"
CONTRACT = ROOT / "tools/workforce_contract.py"


def run_tool(path: Path, *args: str) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(path), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode, output


def registry_candidates() -> list[dict]:
    if not REGISTRY.exists():
        return []

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return data.get("candidates", [])


def security_targets() -> list[dict]:
    return [
        candidate
        for candidate in registry_candidates()
        if candidate.get("status") in {
            "DISCOVERED",
            "RESEARCH_ONLY",
        }
    ]


def run_security() -> tuple[bool, list[str]]:
    failures: list[str] = []

    for candidate in security_targets():
        repository = candidate.get("repository", "")

        if not repository:
            failures.append(f"{candidate.get('name', 'UNKNOWN')}:NO_REPOSITORY")
            continue

        if repository.startswith("http://") or repository.startswith("https://"):
            continue

        target = ROOT / repository

        if not target.exists():
            failures.append(
                f"{candidate.get('name', 'UNKNOWN')}:MISSING:{repository}"
            )
            continue

        code, output = run_tool(SECURITY, str(target))

        if code != 0 or "SECURITY: PASS" not in output:
            failures.append(candidate.get("name", "UNKNOWN"))

    return not failures, failures


def main() -> int:
    if len(sys.argv) < 2:
        print("USAGE: workforce_orchestrator.py <task>")
        return 2

    task = " ".join(sys.argv[1:])

    print("AI_BRIDGE V3 — WORKFORCE ORCHESTRATOR")
    print(f"TASK: {task}")

    candidates = registry_candidates()

    print(f"REGISTRY_CANDIDATES: {len(candidates)}")

    if not candidates:
        print("DISCOVERY: REQUIRED")
        code, output = run_tool(DISCOVERY)

        if output:
            print(output)

        if code != 0:
            print("DECISION: ESCALATE")
            print("REASON: DISCOVERY_FAILED")
            return 2

        candidates = registry_candidates()

    print(f"DISCOVERY: PASS ({len(candidates)} candidates)")

    security_ok, failures = run_security()

    if not security_ok:
        print("SECURITY: FAIL")
        for failure in failures:
            print(f"SECURITY_FAILURE: {failure}")
        print("DECISION: REJECT")
        return 3

    print("SECURITY: PASS")

    code, output = run_tool(SANDBOX)

    if output:
        print(output)

    if code != 0 or "STATUS: READY_FOR_REVIEW" not in output:
        print("SANDBOX: FAIL")
        print("DECISION: REJECT")
        return 4

    print("SANDBOX: PASS")

    code, output = run_tool(CONTRACT)

    if output:
        print(output)

    if code != 0 or "STATUS: PASS" not in output:
        print("CONTRACT: FAIL")
        print("DECISION: REJECT")
        return 5

    print("CONTRACT: PASS")

    code, output = run_tool(SCHEDULER)

    if output:
        print(output)

    if code != 0 or "DECISION: SCHEDULE" not in output:
        print("SCHEDULER: ESCALATE")
        print("DECISION: ESCALATE")
        print("REASON: WORKFORCE_UNAVAILABLE")
        return 6

    print("SCHEDULER: PASS")
    print("SUPERVISOR: INTERNAL")
    print("PROMOTION: NOT_PERFORMED")
    print("DECISION: READY_FOR_EXECUTION")

    return 0


if __name__ == "__main__":
    sys.exit(main())
