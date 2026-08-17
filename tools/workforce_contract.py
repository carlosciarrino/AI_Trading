#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFORCE = ROOT / "docs/workforce"
CONTRACTS = WORKFORCE / "contracts"
CONTRACTS.mkdir(parents=True, exist_ok=True)

STAGES = (
    "RESEARCHER",
    "ANALYST",
    "SECURITY",
    "ARCHITECT",
    "BUILDER",
    "TESTER",
    "REVIEWER",
    "COMMIT",
    "REPORT",
)

STATUSES = (
    "PENDING",
    "RUNNING",
    "PASSED",
    "FAILED",
    "REVIEW_REQUIRED",
    "HUMAN_REQUIRED",
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create(task: str) -> dict:
    return {
        "contract_version": "1.0",
        "mission_id": str(uuid.uuid4()),
        "task": task,
        "created_at": now(),
        "stage": "RESEARCHER",
        "status": "PENDING",
        "agent": None,
        "input": {},
        "output": {},
        "evidence": [],
        "validation": [],
        "next_stage": "RESEARCHER",
        "failure": None,
        "retry": 0,
        "commit": None,
        "human_required": False,
    }


def validate(data: dict) -> tuple[bool, list[str]]:
    errors = []

    required = (
        "contract_version",
        "mission_id",
        "task",
        "created_at",
        "stage",
        "status",
        "input",
        "output",
        "evidence",
        "validation",
        "next_stage",
        "failure",
        "retry",
        "commit",
        "human_required",
    )

    for key in required:
        if key not in data:
            errors.append(f"MISSING:{key}")

    if data.get("stage") not in STAGES:
        errors.append(f"INVALID_STAGE:{data.get('stage')}")

    if data.get("status") not in STATUSES:
        errors.append(f"INVALID_STATUS:{data.get('status')}")

    if not isinstance(data.get("evidence"), list):
        errors.append("INVALID_EVIDENCE")

    if not isinstance(data.get("validation"), list):
        errors.append("INVALID_VALIDATION")

    return not errors, errors


def main() -> int:
    if len(sys.argv) < 2:
        print("USAGE: workforce_contract.py <task> | --validate <file>")
        return 2

    if sys.argv[1] == "--validate":
        if len(sys.argv) != 3:
            print("USAGE: workforce_contract.py --validate <file>")
            return 2

        path = Path(sys.argv[2])
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"STATUS: FAIL")
            print(f"ERROR: {exc}")
            return 1

        ok, errors = validate(data)

        print("AI_BRIDGE V3 — WORKFORCE CONTRACT")
        print(f"FILE: {path}")
        print(f"STATUS: {'PASS' if ok else 'FAIL'}")

        for error in errors:
            print(f"ERROR: {error}")

        return 0 if ok else 1

    task = " ".join(sys.argv[1:])
    data = create(task)
    path = CONTRACTS / f"{data['mission_id']}.json"
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("AI_BRIDGE V3 — WORKFORCE CONTRACT")
    print(f"MISSION_ID: {data['mission_id']}")
    print(f"TASK: {task}")
    print("STAGE: RESEARCHER")
    print("STATUS: PENDING")
    print(f"CONTRACT: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
