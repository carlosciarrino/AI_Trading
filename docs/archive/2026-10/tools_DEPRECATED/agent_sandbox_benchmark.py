#!/usr/bin/env python3

from pathlib import Path
import hashlib
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "sandbox" / "agent_lab" / "baseline"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def prepare_workspace() -> Path:
    workspace = Path(tempfile.mkdtemp(prefix="ai_bridge_agent_"))
    shutil.copytree(BASELINE, workspace / "project")
    return workspace / "project"


def create_task(project: Path) -> Path:
    target = project / "agent_test_target.txt"
    target.write_text(
        "AI_BRIDGE_AGENT_TEST\n"
        "STATUS=ORIGINAL\n",
        encoding="utf-8",
    )
    return target


def test_integrity(target: Path) -> None:
    original = sha256(target)
    backup = target.read_bytes()

    target.write_text(
        "AI_BRIDGE_AGENT_TEST\n"
        "STATUS=MODIFIED\n",
        encoding="utf-8",
    )

    modified = sha256(target)

    if original == modified:
        raise RuntimeError("MODIFICATION TEST FAILED")

    target.write_bytes(backup)

    restored = sha256(target)

    if original != restored:
        raise RuntimeError("RECOVERY TEST FAILED")


def inspect_candidate(name: str) -> None:
    candidate = ROOT / "research" / "external_agents" / name

    print(f"\n===== {name} =====")

    if not candidate.exists():
        print("RESULT: MISSING")
        return

    workspace = prepare_workspace()
    target = create_task(workspace)

    try:
        test_integrity(target)
        print("SANDBOX: PASS")
        print("MODIFICATION: PASS")
        print("RECOVERY: PASS")
    except Exception as exc:
        print(f"RESULT: FAIL: {exc}")
    finally:
        shutil.rmtree(workspace.parent, ignore_errors=True)


def main() -> int:
    if not BASELINE.exists():
        print("ERROR: baseline missing")
        return 1

    for name in (
        "mini-swe-agent",
        "openhands-sdk",
        "aider",
    ):
        inspect_candidate(name)

    print("\n===== BASELINE =====")
    print(BASELINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
