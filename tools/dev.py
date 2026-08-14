#!/usr/bin/env python3
"""
AI_BRIDGE V2 Development Helper
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(*cmd: str) -> int:
    print("\n$", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


def compile_project() -> int:
    files = sorted((ROOT / "core_v2").glob("*.py"))
    return run(
        sys.executable,
        "-m",
        "py_compile",
        *map(str, files),
    )


def bootstrap() -> int:
    return run(sys.executable, "main_v2.py")


def diagnostics() -> int:
    return run(
        sys.executable,
        "diagnostics_v2.py",
        "--report",
    )


def verify() -> int:
    if compile_project():
        return 1

    if bootstrap():
        return 1

    if diagnostics():
        return 1

    if run("git", "diff", "--stat"):
        return 1

    return run("git", "status")


def finish(message: str) -> int:
    if compile_project():
        return 1

    if bootstrap():
        return 1

    if diagnostics():
        return 1

    if run("git", "diff", "--stat"):
        return 1

    if run("git", "status"):
        return 1

    if run("git", "add", "core_v2", "docs", "tools"):
        return 1

    if run("git", "commit", "-m", message):
        return 1

    return run(
        "git",
        "log",
        "--oneline",
        "-5",
    )


def main() -> int:
    parser = argparse.ArgumentParser()

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("verify")

    finish_parser = sub.add_parser("finish")
    finish_parser.add_argument("message")

    args = parser.parse_args()

    if args.command == "verify":
        return verify()

    if args.command == "finish":
        return finish(args.message)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
