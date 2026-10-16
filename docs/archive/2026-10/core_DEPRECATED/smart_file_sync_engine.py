import os
import shutil
import time

from core.atomic_file_engine import AtomicFileEngine


class SmartFileSyncEngine:

    def __init__(self):

        self.shared_dir = "mt4_shared"

        self.mt4_files_dir = (
            "/home/carlo/Scrivania/"
            "XM MT4/MQL4/Files/"
        )

        self.required_files = [

            "ai_signal.txt",
            "ai_confirm.txt",
            "mt4_trades_snapshot.txt"

        ]

        self.atomic = AtomicFileEngine()

    def ensure_directories(self):

        os.makedirs(self.shared_dir, exist_ok=True)

        os.makedirs(self.mt4_files_dir, exist_ok=True)

    def get_time(self, path):

        if not os.path.exists(path):

            return 0

        return os.path.getmtime(path)

    def should_sync(self, src, dst):

        if not os.path.exists(src):

            return False

        return self.get_time(src) > self.get_time(dst)

    def safe_copy(self, src, dst):

        temp = dst + ".tmp"

        shutil.copy2(src, temp)

        os.replace(temp, dst)

    def sync_to_mt4(self):

        for f in self.required_files:

            src = os.path.join(self.shared_dir, f)

            dst = os.path.join(self.mt4_files_dir, f)

            if self.should_sync(src, dst):

                self.safe_copy(src, dst)

                print(f"[SYNC→MT4] {f}")

    def sync_from_mt4(self):

        for f in self.required_files:

            src = os.path.join(self.mt4_files_dir, f)

            dst = os.path.join(self.shared_dir, f)

            if self.should_sync(src, dst):

                self.safe_copy(src, dst)

                print(f"[SYNC←MT4] {f}")

    def full_sync_cycle(self):

        self.ensure_directories()

        self.sync_to_mt4()

        self.sync_from_mt4()

        print("[SMART SYNC] Atomic cycle completed.")
