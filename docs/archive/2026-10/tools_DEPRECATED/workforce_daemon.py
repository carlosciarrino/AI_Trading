#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "docs/workforce/daemon.log"
MAX_CYCLES = 100

LOG.parent.mkdir(parents=True, exist_ok=True)

def run():
    return subprocess.run(
        [sys.executable, "tools/workforce_supervisor.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

for cycle in range(1, MAX_CYCLES + 1):
    result = run()
    output = (result.stdout + result.stderr).strip()

    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"\n===== CYCLE {cycle} =====\n{output}\n")

    print(output)

    if "DECISION: READY_FOR_EXECUTION" in output:
        print("DAEMON: WORK_COMPLETE")
        break

    if "STATUS: HUMAN_REQUIRED" in output:
        print("DAEMON: HUMAN_REQUIRED")
        break

    if result.returncode not in (0, 1):
        print(f"DAEMON: SUPERVISOR_ERROR:{result.returncode}")
        break

    time.sleep(2)
