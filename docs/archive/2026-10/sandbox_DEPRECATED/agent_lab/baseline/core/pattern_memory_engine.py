import json
import os
from datetime import datetime


class PatternMemoryEngine:

    def __init__(self):

        self.file_path = "data/memory/pattern_memory.json"

        self.memory = self.load()

    def load(self):

        if not os.path.exists(self.file_path):

            return {

                "winning_patterns": [],
                "losing_patterns": [],
                "last_update": str(datetime.now())

            }

        with open(self.file_path, "r") as f:

            return json.load(f)

    def save(self):

        self.memory["last_update"] = str(datetime.now())

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w") as f:

            json.dump(self.memory, f, indent=4)

    def store_pattern(self, market_context, performance):

        winrate = performance.get("winrate", 0)

        profit_factor = performance.get("profit_factor", 0)

        pattern = {

            "context": market_context,
            "winrate": winrate,
            "profit_factor": profit_factor,
            "timestamp": str(datetime.now())

        }

        if winrate >= 55 and profit_factor >= 1.2:

            self.memory["winning_patterns"].append(pattern)

            print("[PATTERN MEMORY] Winning pattern stored.")

        else:

            self.memory["losing_patterns"].append(pattern)

            print("[PATTERN MEMORY] Losing pattern stored.")

        self.save()

    def get_best_contexts(self):

        return self.memory["winning_patterns"]

    def get_bad_contexts(self):

        return self.memory["losing_patterns"]
