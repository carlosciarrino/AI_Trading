#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEXT_EXTENSIONS = {
    ".py", ".sh", ".bash", ".zsh", ".js", ".ts",
    ".json", ".yaml", ".yml", ".toml", ".txt",
}

PATTERNS = (
    re.compile(r"\brm\s+-rf\b"),
    re.compile(r"\bsudo\b"),
    re.compile(r"\bcurl\b"),
    re.compile(r"\bwget\b"),
    re.compile(r"\b(?:nc|socat|ssh|scp)\b"),
    re.compile(r"\b(?:eval|exec)\s*\("),
    re.compile(r"chmod\s+777"),
    re.compile(r"base64\s+-d"),
)

CRITICAL_PATTERNS = (
    re.compile(r"\brm\s+-rf\b"),
    re.compile(r"chmod\s+777"),
    re.compile(r"base64\s+-d"),
)

NETWORK_PATTERNS = (
    re.compile(r"\bcurl\b"),
    re.compile(r"\bwget\b"),
    re.compile(r"\b(?:nc|socat|ssh|scp)\b"),
)

PRIVILEGE_PATTERNS = (
    re.compile(r"\bsudo\b"),
)


def severity(path: Path, pattern: re.Pattern[str], line: str) -> str:
    if pattern in CRITICAL_PATTERNS:
        return "CRITICAL"

    if pattern in PRIVILEGE_PATTERNS:
        if ".github/workflows/" in str(path):
            return "REVIEW"
        return "REVIEW"

    if pattern in NETWORK_PATTERNS:
        if ".github/workflows/" in str(path):
            return "REVIEW"
        if "install" in path.name.lower():
            return "REVIEW"
        return "REVIEW"

    if re.search(r"\b(?:eval|exec)\s*\(", line):
        return "REVIEW"

    return "REVIEW"


def inspect(root: Path) -> int:
    root = root.resolve()
    findings = 0
    critical = 0
    review = 0

    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            target = path.resolve(strict=False)
            try:
                target.relative_to(root)
                print(f"SYMLINK_REVIEW:{path.relative_to(root)} -> {target}")
                review += 1
            except ValueError:
                print(f"CRITICAL:SYMLINK_ESCAPE:{path.relative_to(root)} -> {target}")
                critical += 1
            findings += 1
            continue

        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        try:
            lines = path.read_text(
                encoding="utf-8",
                errors="replace",
            ).splitlines()
        except OSError as exc:
            print(f"CRITICAL:UNREADABLE:{path.relative_to(root)}:{exc}")
            critical += 1
            findings += 1
            continue

        for lineno, line in enumerate(lines, 1):
            for pattern in PATTERNS:
                if pattern.search(line):
                    level = severity(path, pattern, line)

                    if level == "CRITICAL":
                        critical += 1
                    else:
                        review += 1

                    findings += 1

                    print(
                        f"{level}:"
                        f"{path.relative_to(root)}:"
                        f"{lineno}:"
                        f"{pattern.pattern}:"
                        f"{line.strip()}"
                    )

    print()
    print("===== SECURITY EVIDENCE =====")
    print(f"FINDINGS: {findings}")
    print(f"CRITICAL: {critical}")
    print(f"REVIEW: {review}")
    print(f"DECISION: {'REJECT' if critical else 'REVIEW_REQUIRED' if review else 'ALLOW'}")

    return 1 if critical else 0


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    return inspect(target)


if __name__ == "__main__":
    raise SystemExit(main())
