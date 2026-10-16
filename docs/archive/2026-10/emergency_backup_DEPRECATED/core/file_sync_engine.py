import os
import shutil


class FileSyncEngine:

    def __init__(self):

        self.shared_dir = "mt4_shared"

        # PATH MT4 REALE USATO

        self.mt4_files_dir = (
            "/home/carlo/Scrivania/"
            "XM MT4/MQL4/Files/"
        )

        self.required_files = [

            "ai_signal.txt",
            "ai_confirm.txt",
            "mt4_trades_snapshot.txt"

        ]

    def ensure_directories(self):

        os.makedirs(
            self.shared_dir,
            exist_ok=True
        )

        os.makedirs(
            self.mt4_files_dir,
            exist_ok=True
        )

        print("[SYNC] Directories verified.")

    def sync_to_mt4(self):

        for file_name in self.required_files:

            source = os.path.join(
                self.shared_dir,
                file_name
            )

            destination = os.path.join(
                self.mt4_files_dir,
                file_name
            )

            if os.path.exists(source):

                shutil.copy2(source, destination)

                print(f"[SYNC] {file_name} -> MT4")

    def sync_from_mt4(self):

        for file_name in self.required_files:

            source = os.path.join(
                self.mt4_files_dir,
                file_name
            )

            destination = os.path.join(
                self.shared_dir,
                file_name
            )

            if os.path.exists(source):

                shutil.copy2(source, destination)

                print(f"[SYNC] MT4 -> {file_name}")

    def full_sync_cycle(self):

        self.ensure_directories()

        self.sync_to_mt4()

        self.sync_from_mt4()
