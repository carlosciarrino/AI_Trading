#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTRACTS = ROOT / "docs/research/AGENT_CONTRACTS.json"
REGISTRY = ROOT / "docs/research/AGENT_REGISTRY.json"


@dataclass(frozen=True)
class DispatchPlan:
    task: str
    roles: tuple[str, ...]
    candidates_required: int
    gates: tuple[str, ...]


ROLE_BY_TASK = {
    "research": ("RESEARCH_AGENT",),
    "security": ("SECURITY_AGENT",),
    "validation": ("VALIDATION_AGENT",),
    "integration": (
        "RESEARCH_AGENT",
        "SECURITY_AGENT",
        "VALIDATION_AGENT",
    ),
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def plan(task: str) -> DispatchPlan:
    roles = ROLE_BY_TASK.get(task)
    if roles is None:
        raise ValueError(f"UNKNOWN_TASK:{task}")

    return DispatchPlan(
        task=task,
        roles=roles,
        candidates_required=len(roles),
        gates=(
            "SECURITY_GATE",
            "SANDBOX_GATE",
            "VALIDATION_GATE",
            "SUPERVISOR_GATE",
        ),
    )


def validate_contract_roles(roles: tuple[str, ...]) -> None:
    available = {
        contract["role"]
        for contract in load(CONTRACTS)["contracts"]
    }

    missing = [role for role in roles if role not in available]

    if missing:
        raise RuntimeError(
            "MISSING_CONTRACTS:" + ",".join(missing)
        )


def candidate_count() -> int:
    data = load(REGISTRY)
    return len(data.get("agents", data.get("candidates", [])))


def main() -> int:
    task = sys.argv[1] if len(sys.argv) > 1 else "integration"

    dispatch = plan(task)
    validate_contract_roles(dispatch.roles)

    available = candidate_count()

    print("AI_BRIDGE V3 — TASK DISPATCHER")
    print(f"TASK: {dispatch.task}")
    print(f"ROLES: {len(dispatch.roles)}")
    for role in dispatch.roles:
        print(f"- {role}")

    print(f"CANDIDATES_AVAILABLE: {available}")
    print(f"CANDIDATES_REQUIRED: {dispatch.candidates_required}")

    if available < dispatch.candidates_required:
        print("DECISION: ESCALATE")
        print("REASON: INSUFFICIENT_CANDIDATES")
        return 2

    print("GATES:")
    for gate in dispatch.gates:
        print(f"- {gate}")

    print("EXECUTION: NOT_PERFORMED")
    print("DECISION: READY_FOR_DISPATCH")
    return 0


if __name__ == "__main__":
    sys.exit(main())
