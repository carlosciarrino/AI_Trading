import json
import os
import shutil
import time


class SelfHealingEngine:

    def __init__(self):

        self.failure_report = (
            "data/logs/failure_report.json"
        )

        self.runtime_state = (
            "data/runtime_state.json"
        )

        self.backup_dir = (
            "data/backups/"
        )

        os.makedirs(self.backup_dir, exist_ok=True)

    def load_failure_report(self):

        if not os.path.exists(self.failure_report):

            return {}

        with open(self.failure_report, "r") as f:

            try:

                return json.load(f)

            except:

                return {}

    def enter_safe_mode(self):

        state = {

            "trading_enabled": False,

            "safe_mode": True,

            "timestamp": time.time()

        }

        with open(self.runtime_state, "w") as f:

            json.dump(state, f, indent=4)

        print("[SELF HEALING] SAFE MODE ENABLED")

    def backup_critical_files(self):

        critical_files = [

            "mt4_shared/ai_signal.txt",
            "mt4_shared/ai_confirm.txt"

        ]

        for file_path in critical_files:

            if os.path.exists(file_path):

                filename = os.path.basename(file_path)

                backup_path = os.path.join(

                    self.backup_dir,
                    filename + ".bak"

                )

                shutil.copy2(file_path, backup_path)

                print(f"[BACKUP] {filename}")

    def repair_missing_file(self, file_path):

        if not os.path.exists(file_path):

            with open(file_path, "w") as f:

                f.write("")

            print(f"[SELF HEALING] Recreated: {file_path}")

    def apply_healing_actions(self, report):

        total_failures = report.get(
            "total_failures",
            0
        )

        categories = report.get(
            "failure_categories",
            {}
        )

        # TROPPI ERRORI → SAFE MODE

        if total_failures >= 3:

            self.enter_safe_mode()

        # BACKUP PREVENTIVO

        self.backup_critical_files()

        # RIPARAZIONE FILE

        self.repair_missing_file(
            "mt4_shared/ai_signal.txt"
        )

        self.repair_missing_file(
            "mt4_shared/ai_confirm.txt"
        )

        # ERRORI CONFERMA

        if categories.get("CONFIRMATION_FAILURE", 0) >= 2:

            print(
                "[SELF HEALING] "
                "Confirmation system unstable."
            )

        # ERRORI SNAPSHOT

        if categories.get("SNAPSHOT_FAILURE", 0) >= 2:

            print(
                "[SELF HEALING] "
                "Snapshot instability detected."
            )

    def execute_self_healing(self):

        report = self.load_failure_report()

        if not report:

            print("[SELF HEALING] No failure report.")

            return

        self.apply_healing_actions(report)

        print("\n[SELF HEALING COMPLETED]\n")
