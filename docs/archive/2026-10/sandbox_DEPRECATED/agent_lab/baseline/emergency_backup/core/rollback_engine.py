import json
import os
import shutil
from datetime import datetime


class RollbackEngine:

    def __init__(self):

        self.rollback_dir = "data/backups/rollback"

        os.makedirs(self.rollback_dir, exist_ok=True)

    def save_safe_strategy(self, strategy):

        filepath = f"{self.rollback_dir}/safe_strategy.json"

        with open(filepath, "w") as file:

            json.dump(strategy, file, indent=4)

        print("[ROLLBACK] Safe strategy saved.")

    def restore_safe_strategy(self):

        filepath = f"{self.rollback_dir}/safe_strategy.json"

        if os.path.exists(filepath):

            with open(filepath, "r") as file:

                strategy = json.load(file)

            print("[ROLLBACK] Safe strategy restored.")

            return strategy

        print("[ROLLBACK] No safe strategy found.")

        return None
