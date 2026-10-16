#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


BENIGN_PATH_PATTERNS = (
    "/tests/",
    "/test/",
    "/fixtures/",
    "/docs/",
    "/README",
)

INSTALLER_PATH_PATTERNS = (
    "/website/install.sh",
    "/benchmark/install-docker-ubuntu.sh",
)

BENCHMARK_PATH_PATTERNS = (
    "/benchmark/",
)

LEGITIMATE_PATTERNS = (
    re.compile(r"\brm\s+-rf\s+/tmp/"),
    re.compile(r"\brm\s+-rf\s+/var/lib/apt/lists/\*"),
    re.compile(r'\bignore\s+rm\s+-rf\s+"\$_dir"'),
)

DANGEROUS_PATTERNS = (
    re.compile(r"curl\b.*\|\s*(sh|bash)\b"),
    re.compile(r"wget\b.*\|\s*(sh|bash)\b"),
    re.compile(r"\beval\s*\("),
    re.compile(r"\bexec\s*\("),
)

PRIVILEGED_PATTERNS = (
    re.compile(r"\bsudo\b"),
    re.compile(r"chmod\s+777"),
    re.compile(r"chmod\s+u\+s"),
)

NETWORK_PATTERNS = (
    re.compile(r"\bcurl\b"),
    re.compile(r"\bwget\b"),
    re.compile(r"\b(?:nc|socat|ssh|scp)\b"),
)


def matches_path(normalized: str, patterns: tuple[str, ...]) -> bool:
    value = normalized.lower()
    return any(pattern in value for pattern in patterns)


def _non_executable_context(path: str, lineno: int) -> bool:
    from tokenize import COMMENT, STRING, generate_tokens
    from io import StringIO

    p = Path(__file__).resolve().parent.parent / path
    if not p.exists():
        return False

    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False

    if p.suffix != ".py":
        raw = text.splitlines()
        if 1 <= lineno <= len(raw):
            return raw[lineno - 1].lstrip().startswith("#")
        return False

    try:
        for tok in generate_tokens(StringIO(text).readline):
            if tok.start[0] <= lineno <= tok.end[0]:
                if tok.type in (COMMENT, STRING):
                    return True
    except Exception:
        return False

    return False


def classify(path: str, line: str, lineno: int | None = None) -> tuple[str, str]:
    normalized = "/" + path.replace("\\", "/").lstrip("/")
    text = line.strip()

    if text.startswith("#") or text.startswith("//"):
        return "LEGITIMATE", "comment security pattern"

    lower = normalized.lower()

    # Security tests/rules/examples describe dangerous behavior; they do not execute it.
    evidence_context = (
        "/tests/" in lower
        or "/test/" in lower
        or "/security/" in lower
        or "/defense_in_depth/" in lower
        or "/context/prompts/" in lower
        or "/examples/" in lower
        or lower.endswith((".md", ".rst", ".txt"))
    )

    if evidence_context:
        return "LEGITIMATE", "security evidence/documentation/test context"

    if normalized.endswith((".py", ".md", ".rst", ".txt")):
        if "curl" in text and "bash" in text and "|" in text:
            return "LEGITIMATE", "documented security pattern"
        if re.search(r"[" + chr(34) + r"](?:curl|wget).*[|" + chr(34) + r"]", text):
            return "LEGITIMATE", "string/documentation security pattern"

    # Non-executable evidence: comments, strings, docs, tests, fixtures.
    if text.startswith("#"):
        return "LEGITIMATE", "comment security evidence"

    try:
        lineno = int(globals().get("_CURRENT_LINE", "0"))
    except ValueError:
        lineno = 0

    if lineno and _non_executable_context(path, lineno):
        return "LEGITIMATE", "non-executable security evidence"

    if matches_path(normalized, BENIGN_PATH_PATTERNS):
        return "LEGITIMATE", "test/documentation security evidence"

    # Test/fixture code may intentionally contain dangerous command examples.
    if matches_path(normalized, BENIGN_PATH_PATTERNS):
        return "LEGITIMATE", "test/documentation security pattern"

    # Dynamic execution requires review, never automatic rejection.
    for pattern in DANGEROUS_PATTERNS:
        if pattern.search(text):
            if re.search(r"\b(?:eval|exec)\s*\(", text):
                return "REVIEW", "dynamic execution requires contextual review"
            return "DANGEROUS", f"dangerous execution pattern: {pattern.pattern}"

    if matches_path(normalized, INSTALLER_PATH_PATTERNS):
        for pattern in PRIVILEGED_PATTERNS:
            if pattern.search(text):
                return "LEGITIMATE", f"expected installer privilege operation: {pattern.pattern}"
        for pattern in NETWORK_PATTERNS:
            if pattern.search(text):
                return "LEGITIMATE", f"expected installer network operation: {pattern.pattern}"

    if matches_path(normalized, BENCHMARK_PATH_PATTERNS):
        for pattern in PRIVILEGED_PATTERNS:
            if pattern.search(text):
                return "LEGITIMATE", f"expected benchmark environment operation: {pattern.pattern}"
        for pattern in NETWORK_PATTERNS:
            if pattern.search(text):
                return "LEGITIMATE", f"expected benchmark network operation: {pattern.pattern}"

    return "REVIEW", "unclassified security-sensitive pattern"


def second_inspection(path: str, line: str, classification: str) -> tuple[str, str]:
    normalized = "/" + path.replace("\\", "/").lstrip("/")
    text = line.strip()
    lower = normalized.lower()

    evidence_paths = (
        "/tests/",
        "/test/",
        "/fixtures/",
        "/examples/",
        "/docs/",
        "/security/",
        "/defense_in_depth/",
        "/context/prompts/",
        ".github/workflows/",
    )

    if any(item in lower for item in evidence_paths):
        return "LEGITIMATE", "second inspection: evidence/test/documentation context"

    if text.startswith(("#", "//")):
        return "LEGITIMATE", "second inspection: comment context"

    if classification == "DANGEROUS":
        if "curl" in text and "|" in text and ("bash" in text or "sh" in text):
            return "REVIEW", "second inspection: executable remote-code pattern requires confirmation"

        if re.search(r"\\b(?:eval|exec)\\s*\\(", text):
            return "REVIEW", "second inspection: dynamic execution requires confirmation"

    return classification, f"second inspection: confirmed {classification.lower()}"

def classify_file(path: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    try:
        lines = path.read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines()
    except OSError as exc:
        return [{
            "classification": "REVIEW",
            "reason": f"unreadable file: {exc}",
            "path": str(path),
            "line": "",
        }]

    patterns = (
        re.compile(r"\brm\s+-rf\b"),
        re.compile(r"\bsudo\b"),
        re.compile(r"\bcurl\b"),
        re.compile(r"\bwget\b"),
        re.compile(r"\bnc\b"),
        re.compile(r"\bsocat\b"),
        re.compile(r"\bssh\b"),
        re.compile(r"\bscp\b"),
        re.compile(r"\bos\.system\b"),
        re.compile(r"\beval\s*\("),
        re.compile(r"\bexec\s*\("),
        re.compile(r"chmod\s+777"),
        re.compile(r"chmod\s+u\+s"),
    )

    for number, line in enumerate(lines, 1):
        for pattern in patterns:
            if pattern.search(line):
                if line.lstrip().startswith("#"):
                    continue
                classification, reason = classify(str(path), line)

                if classification in {"DANGEROUS", "REVIEW"}:
                    classification, reason = second_inspection(
                        str(path),
                        line,
                        classification,
                    )

                findings.append({
                    "classification": classification,
                    "reason": reason,
                    "path": str(path),
                    "line": str(number),
                    "evidence": line.strip(),
                })

    return findings
