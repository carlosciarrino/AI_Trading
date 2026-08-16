#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs/research/AGENT_REGISTRY.json"

ROLE_REQUIREMENTS = {
    "RESEARCH_AGENT": {"agent", "local", "git"},
    "SECURITY_AGENT": {"agent", "sandbox", "docker"},
    "VALIDATION_AGENT": {"agent", "testing", "git"},
}


def load_candidates() -> list[dict]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return data.get("candidates", [])


def compatible(candidate: dict, role: str) -> bool:
    return ROLE_REQUIREMENTS[role].issubset(
        set(candidate.get("capabilities", []))
    )


def schedule(candidates: list[dict]) -> dict[str, dict | None]:
    result: dict[str, dict | None] = {}
    used: set[str] = set()

    for role in ROLE_REQUIREMENTS:
        matches = [
            c for c in candidates
            if c["name"] not in used
            and compatible(c, role)
        ]

        if not matches:
            result[role] = None
            continue

        candidate = sorted(
            matches,
            key=lambda c: (
                c.get("status") != "RESEARCH_ONLY",
                c["name"],
            ),
        )[0]

        result[role] = candidate
        used.add(candidate["name"])

    return result


def main() -> int:
    candidates = load_candidates()
    assignments = schedule(candidates)

    print("AI_BRIDGE V3 — WORKFORCE SCHEDULER")
    print(f"CANDIDATES: {len(candidates)}")

    failed = False

    for role, candidate in assignments.items():
        if candidate is None:
            print(f"{role}: NONE")
            failed = True
        else:
            print(
                f"{role}: {candidate['name']} "
                f"[{candidate.get('status', 'UNKNOWN')}]"
            )

    print("SUPERVISOR: INTERNAL")

    if failed:
        print("DECISION: ESCALATE")
        print("REASON: INSUFFICIENT_UNIQUE_CANDIDATES")
        return 2

    print("DECISION: SCHEDULE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
