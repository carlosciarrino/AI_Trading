#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTRACTS = ROOT / "docs/research/AGENT_CONTRACTS.json"


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class AgentContract:
    role: str
    mission: str
    inputs: list[str]
    checklist: list[str]
    forbidden_actions: list[str]
    required_evidence: list[str]
    pass_conditions: list[str]
    fail_conditions: list[str]
    escalation: list[str]


DEFAULT_CONTRACTS = [
    AgentContract(
        role="RESEARCH_AGENT",
        mission="Find existing reusable projects matching task.",
        inputs=["task", "repository", "constraints"],
        checklist=[
            "Identify candidate",
            "Verify source repository",
            "Verify license",
            "Verify maintenance status",
            "Verify architecture fit",
            "Verify dependency fit",
            "Record strengths",
            "Record weaknesses",
        ],
        forbidden_actions=[
            "Modify core_v2",
            "Execute candidate code outside sandbox",
            "Promote candidate",
        ],
        required_evidence=[
            "repository URL",
            "license evidence",
            "candidate capabilities",
            "fit assessment",
        ],
        pass_conditions=["All mandatory checks completed", "Evidence complete"],
        fail_conditions=["Missing source evidence", "License incompatible"],
        escalation=["Ambiguous license", "Architecture incompatibility"],
    ),
    AgentContract(
        role="SECURITY_AGENT",
        mission="Detect malicious, unsafe, hidden, or project-destructive behavior.",
        inputs=["candidate repository", "security rules"],
        checklist=[
            "Scan hidden files",
            "Scan symlinks",
            "Scan executable files",
            "Scan network commands",
            "Scan shell execution",
            "Scan privilege escalation",
            "Scan destructive commands",
            "Scan encoded payloads",
            "Scan secrets",
            "Inspect critical findings",
        ],
        forbidden_actions=[
            "Modify candidate",
            "Execute untrusted candidate code",
            "Approve own findings",
        ],
        required_evidence=["file count", "findings", "critical findings", "decision"],
        pass_conditions=["No unresolved critical findings"],
        fail_conditions=["Critical unresolved finding"],
        escalation=["Any uncertain security finding"],
    ),
    AgentContract(
        role="VALIDATION_AGENT",
        mission="Verify candidate behavior and integration suitability in sandbox.",
        inputs=["security-approved candidate", "task contract"],
        checklist=[
            "Create isolated workspace",
            "Run declared validation",
            "Check baseline integrity",
            "Check required behavior",
            "Check regression risk",
            "Produce reproducible evidence",
        ],
        forbidden_actions=[
            "Modify protected core_v2",
            "Promote candidate",
            "Bypass security gate",
        ],
        required_evidence=["validation commands", "results", "integrity result"],
        pass_conditions=["All mandatory validation passes"],
        fail_conditions=["Validation failure", "Integrity failure"],
        escalation=["Environment-dependent failure"],
    ),
    AgentContract(
        role="SUPERVISOR",
        mission="Coordinate workforce and enforce gates.",
        inputs=["agent reports", "task contract"],
        checklist=[
            "Verify contract completeness",
            "Verify required evidence",
            "Verify Security Gate",
            "Verify Validation Gate",
            "Reject incomplete reports",
            "Select qualified agent",
            "Prepare promotion decision",
        ],
        forbidden_actions=[
            "Bypass failed gate",
            "Treat WARNING as PASS",
            "Promote without evidence",
        ],
        required_evidence=["agent reports", "gate results", "final decision"],
        pass_conditions=["All required gates PASS"],
        fail_conditions=["Missing evidence", "Failed mandatory gate"],
        escalation=["Strategic decision required"],
    ),
]


def save() -> None:
    CONTRACTS.parent.mkdir(parents=True, exist_ok=True)
    CONTRACTS.write_text(
        json.dumps(
            {"version": 1, "contracts": [asdict(c) for c in DEFAULT_CONTRACTS]},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    save()
    print("AI_BRIDGE V3 — AGENT CONTRACTS")
    print(f"CONTRACTS: {len(DEFAULT_CONTRACTS)}")
    print(f"OUTPUT: {CONTRACTS.relative_to(ROOT)}")
    print("STATUS: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
