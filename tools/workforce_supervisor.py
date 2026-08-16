#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACTS = ROOT / "docs/research/AGENT_CONTRACTS.json"
REGISTRY = ROOT / "docs/research/AGENT_REGISTRY.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(role: str, report: dict) -> tuple[str, list[str]]:
    if role not in {c["role"] for c in load(CONTRACTS)["contracts"]}:
        return "REJECT", ["UNKNOWN_ROLE"]

    required = {
        "RESEARCH_AGENT": ["source", "license", "fit"],
        "SECURITY_AGENT": ["file_count", "findings", "decision"],
        "VALIDATION_AGENT": ["results", "integrity"],
        "SUPERVISOR": ["reports", "gates", "decision"],
    }[role]

    missing = [key for key in required if key not in report]
    if missing:
        return "REJECT", [f"MISSING:{key}" for key in missing]

    if any(report[key] in ("FAIL", "BLOCKED") for key in report if isinstance(report[key], str)):
        return "REJECT", ["FAILED_GATE"]

    return "PASS", []


def candidates() -> list[dict]:
    data = load(REGISTRY)
    return data.get("agents", data.get("candidates", []))


def main() -> int:
    print("AI_BRIDGE V3 — WORKFORCE SUPERVISOR")
    print(f"CONTRACTS: {len(load(CONTRACTS)['contracts'])}")
    print(f"CANDIDATES: {len(candidates())}")
    print("WORKFORCE: DYNAMIC")
    print("SECURITY_GATE: REQUIRED")
    print("VALIDATION_GATE: REQUIRED")
    print("PROMOTION_GATE: REQUIRED")
    print("STATUS: READY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
