#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_FILES = 10000

TEXT_SUFFIXES = {
    ".py", ".sh", ".bash", ".zsh", ".js", ".ts",
    ".json", ".yaml", ".yml", ".toml", ".txt",
    ".md", ".html", ".css", ".ini", ".cfg",
}

SAFE_HIDDEN = {
    ".gitignore",
    ".dockerignore",
    ".gitkeep",
}

PATTERNS = (
    ("rm_rf", re.compile(r"\brm\s+-rf\b")),
    ("sudo", re.compile(r"\bsudo\b")),
    ("curl", re.compile(r"\bcurl\b")),
    ("wget", re.compile(r"\bwget\b")),
    ("network", re.compile(r"\b(?:nc|socat|ssh|scp)\b")),
    ("exec", re.compile(r"\bexec\s*\(")),
    ("eval", re.compile(r"\beval\s*\(")),
    ("chmod_777", re.compile(r"\bchmod\s+777\b")),
    ("base64_decode", re.compile(r"\bbase64\s+-d\b")),
    ("secret", re.compile(
        r"\b(?:api[_-]?key|secret[_-]?key|password|token|private[_-]?key)\b",
        re.IGNORECASE,
    )),
)

CRITICAL_MARKERS = (
    "credential exfiltration",
    "steal credentials",
    "send credentials",
    "upload secrets",
    "reverse shell",
    "persistence",
)

SAFE_METADATA_PARTS = {
    ".git",
}

BENIGN_PARTS = {
    "test",
    "tests",
    "fixtures",
    "docs",
    "documentation",
}


def classify(path: Path, kind: str, text: str) -> str:
    parts = set(path.parts)
    suffix = path.suffix.lower()
    lowered = text.lower()

    if any(part in SAFE_METADATA_PARTS for part in path.parts):
        return "SAFE_METADATA"

    if any(marker in lowered for marker in CRITICAL_MARKERS):
        return "CRITICAL"

    if kind == "path_escape":
        return "CRITICAL"

    if kind == "symlink":
        return "REVIEW"

    if kind == "chmod_777":
        return "HIGH"

    if kind == "secret":
        return "HIGH"

    if kind in {"rm_rf", "exec", "eval", "network"}:
        if any(part in BENIGN_PARTS for part in path.parts):
            return "BENIGN"
        if suffix in {".md", ".txt", ".json", ".yaml", ".yml"}:
            return "REVIEW"
        return "HIGH"

    if kind in {"sudo", "curl", "wget"}:
        if ".github" in parts and "workflows" in parts:
            return "REVIEW"
        if "install" in path.name.lower() or "benchmark" in parts:
            return "REVIEW"
        return "BENIGN"

    if any(part in BENIGN_PARTS for part in path.parts):
        return "BENIGN"

    return "REVIEW"


def scan(root: Path) -> tuple[list[str], list[str], dict[str, int]]:
    findings: list[str] = []
    files: list[str] = []
    counts = {
        "SAFE_METADATA": 0,
        "BENIGN": 0,
        "REVIEW": 0,
        "HIGH": 0,
        "CRITICAL": 0,
    }

    root = root.resolve()

    for path in root.rglob("*"):
        if len(files) >= MAX_FILES:
            findings.append("CRITICAL:FILE_LIMIT_EXCEEDED")
            counts["CRITICAL"] += 1
            break

        try:
            rel = path.relative_to(root)
        except ValueError:
            findings.append(f"CRITICAL:PATH_ESCAPE:{path}")
            counts["CRITICAL"] += 1
            continue

        if path.is_symlink():
            classification = classify(rel, "symlink", "")
            counts[classification] += 1
            findings.append(f"{classification}:SYMLINK:{rel}")
            continue

        if not path.is_file():
            continue

        files.append(str(rel))

        if any(part.startswith(".") for part in rel.parts):
            if path.name not in SAFE_HIDDEN:
                classification = (
                    "SAFE_METADATA"
                    if ".git" in rel.parts
                    else "REVIEW"
                )
                counts[classification] += 1
                findings.append(f"{classification}:HIDDEN_FILE:{rel}")

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except OSError:
            counts["REVIEW"] += 1
            findings.append(f"REVIEW:UNREADABLE:{rel}")
            continue

        for kind, pattern in PATTERNS:
            if not pattern.search(text):
                continue

            classification = classify(rel, kind, text)
            counts[classification] += 1
            findings.append(
                f"{classification}:{rel}:{pattern.pattern}"
            )

    return files, findings, counts


def main() -> int:
    if len(sys.argv) != 2:
        print("USAGE: agent_security.py <target>")
        return 2

    target = Path(sys.argv[1])

    if not target.exists():
        print(f"TARGET_NOT_FOUND:{target}")
        return 2

    files, findings, counts = scan(target)

    print("AI_BRIDGE V3 — SECURITY GATE")
    print("TARGET: PASS")
    print(f"FILES: {len(files)}")
    print(f"CRITICAL: {counts['CRITICAL']}")
    print(f"HIGH: {counts['HIGH']}")
    print(f"REVIEW: {counts['REVIEW']}")
    print(f"BENIGN: {counts['BENIGN']}")
    print(f"SAFE_METADATA: {counts['SAFE_METADATA']}")

    for finding in findings:
        print(finding)

    if counts["CRITICAL"] or counts["HIGH"]:
        print("SECURITY: FAIL")
        print("DECISION: REJECT")
        return 1

    if counts["REVIEW"]:
        print("SECURITY: REVIEW_REQUIRED")
        print("DECISION: REVIEW")
        return 3

    print("SECURITY: PASS")
    print("DECISION: ALLOW_SANDBOX")
    return 0


if __name__ == "__main__":
    sys.exit(main())
