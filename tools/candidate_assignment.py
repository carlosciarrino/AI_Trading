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

WORKER_ROLES = set(ROLE_REQUIREMENTS)


def load_registry() -> list[dict]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return data.get("candidates", [])


def compatible(candidate: dict, role: str) -> bool:
    required = ROLE_REQUIREMENTS[role]
    capabilities = set(candidate.get("capabilities", []))
    return required.issubset(capabilities)


def assign(candidates: list[dict]) -> dict[str, dict | None]:
    assignments: dict[str, dict | None] = {}

    for role, required in ROLE_REQUIREMENTS.items():
        matches = [
            candidate
            for candidate in candidates
            if compatible(candidate, role)
        ]

        if not matches:
            assignments[role] = None
            continue

        assignments[role] = sorted(
            matches,
            key=lambda candidate: (
                candidate.get("status") != "RESEARCH_ONLY",
                candidate["name"],
            ),
        )[0]

    return assignments


def main() -> int:
    candidates = load_registry()
    assignments = assign(candidates)

    print("AI_BRIDGE V3 — CANDIDATE ASSIGNMENT")
    print(f"CANDIDATES: {len(candidates)}")

    failed = False

    for role in ROLE_REQUIREMENTS:
        candidate = assignments[role]

        if candidate is None:
            print(f"{role}: NONE")
            failed = True
            continue

        print(
            f"{role}: {candidate['name']} "
            f"[{candidate.get('status', 'UNKNOWN')}]"
        )

    print("SUPERVISOR: INTERNAL")

    if failed:
        print("DECISION: ESCALATE")
        return 2

    print("DECISION: ASSIGN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
