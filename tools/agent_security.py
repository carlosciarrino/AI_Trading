#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


MAX_FILES = 10000

ALLOWED_HIDDEN = {
    ".gitignore",
    ".dockerignore",
    ".gitkeep",
}

ALLOWED_HIDDEN_DIRS = {
    ".git",
    ".github",
}

CRITICAL = (
    re.compile(r"\brm\s+-rf\b"),
    re.compile(r"\bsudo\b"),
    re.compile(r"chmod\s+777"),
    re.compile(r"base64\s+-d"),
)

WARNING = (
    re.compile(r"\bcurl\b"),
    re.compile(r"\bwget\b"),
    re.compile(r"\bnc\b"),
    re.compile(r"\bsocat\b"),
    re.compile(r"\bssh\b"),
    re.compile(r"\bscp\b"),
    re.compile(r"\beval\s*\("),
    re.compile(r"\bexec\s*\("),
)

TEXT_SUFFIXES = {
    ".py",
    ".sh",
    ".bash",
    ".zsh",
    ".js",
    ".ts",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".txt",
}


def classify(path: Path, pattern: re.Pattern[str]) -> str:
    name = path.as_posix()

    if (
        name.startswith(".github/workflows/")
        and pattern.pattern in {
            r"\bcurl\b",
            r"\bwget\b",
            r"\bsudo\b",
        }
    ):
        return "BENIGN_CONTEXT"

    if (
        "/benchmarks/" in name
        or "/benchmark" in name
    ) and pattern.pattern in {
        r"\bcurl\b",
        r"\bwget\b",
        r"\bexec\s*\(",
    }:
        return "BENIGN_CONTEXT"

    return "WARNING"


def scan(root: Path) -> tuple[list[str], list[str], list[str]]:
    critical: list[str] = []
    warnings: list[str] = []
    files: list[str] = []

    root = root.resolve()

    for path in root.rglob("*"):
        if len(files) >= MAX_FILES:
            critical.append("FILE_LIMIT_EXCEEDED")
            break

        try:
            rel = path.relative_to(root)
        except ValueError:
            critical.append(f"PATH_ESCAPE:{path}")
            continue

        if path.is_symlink():
            critical.append(f"SYMLINK:{rel}")
            continue

        if not path.is_file():
            continue

        files.append(str(rel))

        hidden_parts = [
            part for part in rel.parts
            if part.startswith(".")
        ]

        if hidden_parts:
            if (
                path.name not in ALLOWED_HIDDEN
                and not any(
                    part in ALLOWED_HIDDEN_DIRS
                    for part in hidden_parts
                )
            ):
                if path.name.startswith(".") and path.name not in {
                    ".env",
                    ".env.local",
                    ".env.production",
                }:
                    if rel.parent == Path("."):
                        warnings.append(
                            f"METADATA:{rel}"
                        )
                else:
                    critical.append(f"HIDDEN_FILE:{rel}")

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except OSError:
            critical.append(f"UNREADABLE:{rel}")
            continue

        for pattern in CRITICAL:
            if pattern.search(text):
                critical.append(
                    f"CRITICAL:{rel}:{pattern.pattern}"
                )

        for pattern in WARNING:
            if pattern.search(text):
                classification = classify(rel, pattern)
                if classification == "BENIGN_CONTEXT":
                    warnings.append(
                        f"BENIGN:{rel}:{pattern.pattern}"
                    )
                else:
                    warnings.append(
                        f"WARNING:{rel}:{pattern.pattern}"
                    )

    return files, critical, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print(
            "usage: python3 tools/agent_security.py <target>",
            file=sys.stderr,
        )
        return 2

    target = Path(sys.argv[1])

    if not target.exists():
        print(f"TARGET: FAIL\nERROR: NOT_FOUND:{target}")
        return 2

    files, critical, warnings = scan(target)

    print("AI_BRIDGE V3 — SECURITY GATE")
    print(f"TARGET: PASS")
    print(f"FILES: {len(files)}")
    print(f"CRITICAL: {len(critical)}")
    print(f"WARNING: {len(warnings)}")
    print(f"SECURITY: {'FAIL' if critical else 'PASS'}")
    print(
        f"DECISION: {'REJECT' if critical else 'ALLOW_SANDBOX'}"
    )

    if critical:
        print("\n===== CRITICAL =====")
        for finding in critical:
            print(finding)

    if warnings:
        print("\n===== WARNINGS =====")
        for finding in warnings:
            print(finding)

    return 1 if critical else 0


if __name__ == "__main__":
    raise SystemExit(main())
