#!/usr/bin/env python3

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "research" / "external_agents"


def run(cmd: list[str], cwd: Path) -> str:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.stdout.strip()


def inspect_candidate(path: Path) -> None:
    print(f"\n===== {path.name} =====")

    pyproject = path / "pyproject.toml"
    readme = path / "README.md"
    license_file = path / "LICENSE"
    license_md = path / "LICENSE.md"

    print(f"path: {path}")

    if license_file.exists():
        print("license_file: LICENSE")
        print(license_file.read_text(errors="replace")[:120])
    elif license_md.exists():
        print("license_file: LICENSE.md")
        print(license_md.read_text(errors="replace")[:120])
    else:
        print("license_file: NOT FOUND")

    if pyproject.exists():
        text = pyproject.read_text(errors="replace")

        name = re.search(
            r'(?m)^name\s*=\s*"([^"]+)"',
            text,
        )
        python = re.search(
            r'(?m)^requires-python\s*=\s*"([^"]+)"',
            text,
        )

        print(f"package: {name.group(1) if name else 'UNKNOWN'}")
        print(
            "python: "
            f"{python.group(1) if python else 'NOT DECLARED'}"
        )

    print(
        "git_head: "
        + run(["git", "rev-parse", "HEAD"], path)
    )

    print(
        "git_status: "
        + (run(["git", "status", "--short"], path) or "CLEAN")
    )

    if readme.exists():
        readme_text = readme.read_text(errors="replace")
        keywords = (
            "sandbox",
            "docker",
            "local",
            "agent",
            "mcp",
            "model",
            "test",
            "git",
        )

        print("capability_keywords:")
        lowered = readme_text.lower()

        for keyword in keywords:
            print(
                f"  {keyword}: "
                f"{'YES' if keyword in lowered else 'NO'}"
            )


def main() -> int:
    if not CANDIDATES.exists():
        print("ERROR: candidate directory not found")
        return 1

    candidates = sorted(
        path for path in CANDIDATES.iterdir()
        if path.is_dir() and (path / ".git").exists()
    )

    if not candidates:
        print("ERROR: no candidate repositories found")
        return 1

    print("AI_BRIDGE V3 — AGENT CANDIDATE INSPECTOR")
    print(f"Candidates: {len(candidates)}")

    for candidate in candidates:
        inspect_candidate(candidate)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
