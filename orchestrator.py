import os
import time
from datetime import datetime

from core.self_repair import SelfRepair
from core.state_manager import StateManager
from core.watchdog import Watchdog


class Orchestrator:

    def __init__(self):

        self.state = StateManager()
        self.repair = SelfRepair()
        self.watchdog = Watchdog()

        self.running = True

    def startup_check(self):

        print("\n[ORCHESTRATOR] Startup system check...\n")

        self.repair.check_critical_files()

        self.state.load_state()

        self.watchdog.system_health()

        print("\n[ORCHESTRATOR] System ready.\n")

    def main_loop(self):

        print("[ORCHESTRATOR] Running...\n")

        while self.running:

            try:

                self.watchdog.system_health()

                self.repair.quick_repair()

                self.state.save_runtime_state()

                time.sleep(10)

            except Exception as e:

                print(f"[ORCHESTRATOR ERROR] {e}")

                time.sleep(5)
