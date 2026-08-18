#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from security_policy import classify as policy_classify, second_inspection

ROOT = Path(__file__).resolve().parent.parent

EVIDENCE = ROOT / "tools/security_evidence.py"
REPORT_DIR = ROOT / "docs/research/security"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

LEGITIMATE_CONTEXT = (
    ".github/workflows/",
    "tests/",
    "test_",
    "tests/fixtures/",
    "benchmark/",
    "docs/",
    "README",
    "CONTRIBUTING",
)

NETWORK_PATTERNS = (
    r"\bcurl\b",
    r"\bwget\b",
    r"\b(?:nc|socat|ssh|scp)\b",
)

DANGEROUS_PATTERNS = (
    r"\brm\s+-rf\s+/",
    r"\brm\s+-rf\s+\$",
    r"chmod\s+777",
    r"base64\s+-d",
)


def classify(path: str, line: str, pattern: str) -> tuple[str, str]:
    return policy_classify(path, line)


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT

    result = subprocess.run(
        [sys.executable, str(EVIDENCE), str(target)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    findings = []

    for raw in result.stdout.splitlines():
        if not raw.startswith(("CRITICAL:", "REVIEW:")):
            continue

        parts = raw.split(":", 4)
        if len(parts) < 5:
            continue

        level, path, lineno, pattern, line = parts

        import security_policy
        security_policy._CURRENT_LINE = lineno
        classification, reason = classify(path, line, pattern)

        if classification in {"DANGEROUS", "REVIEW"}:
            classification, reason = second_inspection(
                path,
                line,
                classification,
            )

        if classification == "REVIEW":
            classification = "UNKNOWN"

        findings.append(
            {
                "path": path,
                "line": int(lineno),
                "pattern": pattern,
                "source_level": level,
                "classification": classification,
                "reason": reason,
                "evidence": line,
            }
        )

    counts = {
        "MALICIOUS": 0,
        "DANGEROUS": 0,
        "LEGITIMATE": 0,
        "UNKNOWN": 0,
    }

    for item in findings:
        counts[item["classification"]] += 1

    if counts["MALICIOUS"] or counts["DANGEROUS"]:
        decision = "REJECT"
    elif counts["UNKNOWN"]:
        decision = "REVIEW"
    else:
        decision = "ALLOW"

    report = {
        "target": str(target),
        "findings": findings,
        "counts": counts,
        "decision": decision,
    }

    output = REPORT_DIR / "latest.json"
    output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("AI_BRIDGE V3 — SECURITY CLASSIFIER")
    print(f"TARGET: {target}")
    print(f"FINDINGS: {len(findings)}")

    for key, value in counts.items():
        print(f"{key}: {value}")

    print(f"DECISION: {decision}")
    print(f"REPORT: {output}")

    return 1 if decision == "REJECT" else 0


if __name__ == "__main__":
    raise SystemExit(main())
