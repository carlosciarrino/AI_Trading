#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "sandbox" / "agent_lab" / "baseline"
REGISTRY = ROOT / "docs" / "research" / "AGENT_REGISTRY.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def snapshot_tree(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): sha256(path)
        for path in sorted(root.rglob("*"))
        if (
            path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix not in {".pyc", ".pyo"}
        )
    }


def create_workspace() -> Path:
    if not BASELINE.exists():
        raise RuntimeError("BASELINE_MISSING")

    workspace = Path(
        tempfile.mkdtemp(prefix="ai_bridge_supervisor_")
    )
    shutil.copytree(BASELINE, workspace / "project")
    return workspace / "project"


def run_validation(project: Path) -> None:
    files = sorted((project / "core_v2").glob("*.py"))

    if not files:
        raise RuntimeError("CORE_FILES_MISSING")

    subprocess.run(
        [
            "python3",
            "-m",
            "py_compile",
            *map(str, files),
        ],
        check=True,
        cwd=project,
    )


def register_candidate(
    name: str,
    repository: str,
    license_name: str,
    capabilities: list[str],
) -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)

    if REGISTRY.exists():
        data = json.loads(
            REGISTRY.read_text(encoding="utf-8")
        )
    else:
        data = {"candidates": []}

    candidates = data.setdefault("candidates", [])

    candidate = {
        "name": name,
        "repository": repository,
        "license": license_name,
        "capabilities": capabilities,
        "status": "RESEARCH_ONLY",
    }

    candidates = [
        item
        for item in candidates
        if item.get("name") != name
    ]

    candidates.append(candidate)
    data["candidates"] = candidates

    REGISTRY.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    print("AI_BRIDGE V3 — SUPERVISOR")

    before = snapshot_tree(BASELINE)

    workspace = create_workspace()

    try:
        run_validation(workspace)

        after = snapshot_tree(workspace)

        if before != after:
            added = sorted(set(after) - set(before))
            removed = sorted(set(before) - set(after))
            changed = sorted(
                path
                for path in set(before) & set(after)
                if before[path] != after[path]
            )

            print(f"ADDED: {added}")
            print(f"REMOVED: {removed}")
            print(f"CHANGED: {changed}")

            raise RuntimeError("BASELINE_CHANGED")

        print("BASELINE: PASS")
        print("VALIDATION: PASS")
        print("WORKSPACE: PASS")
        print("PROMOTION: NOT PERFORMED")

    finally:
        shutil.rmtree(
            workspace.parent,
            ignore_errors=True,
        )

    register_candidate(
        "mini-swe-agent",
        "research/external_agents/mini-swe-agent",
        "MIT",
        [
            "agent",
            "sandbox",
            "docker",
            "local",
            "git",
            "testing",
        ],
    )

    register_candidate(
        "openhands-sdk",
        "research/external_agents/openhands-sdk",
        "MIT",
        [
            "agent",
            "docker",
            "local",
            "git",
            "testing",
            "mcp",
        ],
    )

    register_candidate(
        "aider",
        "research/external_agents/aider",
        "UNKNOWN",
        [
            "agent",
            "local",
            "git",
            "testing",
        ],
    )

    print("REGISTRY: UPDATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
