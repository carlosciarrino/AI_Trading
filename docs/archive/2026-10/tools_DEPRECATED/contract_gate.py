#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "docs/workforce/OPERATING_CONTRACT.md"

REQUIRED = (
    "APPROVED decision = binding immediately",
    "Binding decisions must be persisted in repository",
    "Repository = source of truth",
    "Chat = coordination surface only",
    "Never re-open resolved decisions unless concrete technical evidence requires change",
    "Known failure classes must use existing recovery procedure",
    "Minimize human copy/paste",
    "Prefer one aggregated terminal command",
    "HUMAN_REQUIRED",
)

def main():
    if not CONTRACT.exists():
        print("CONTRACT_GATE: FAIL")
        print("REASON: CONTRACT_MISSING")
        return 2

    text = CONTRACT.read_text(encoding="utf-8")
    missing = [x for x in REQUIRED if x not in text]

    if missing:
        print("CONTRACT_GATE: FAIL")
        print("MISSING:")
        for item in missing:
            print(item)
        return 3

    print("CONTRACT_GATE: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
