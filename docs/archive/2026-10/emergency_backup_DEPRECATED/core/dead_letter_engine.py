import json
import os


class DeadLetterEngine:

    def __init__(self):

        self.dead_letter_file = (
            "data/logs/dead_letter_queue.json"
        )

        os.makedirs("data/logs", exist_ok=True)

    def save_failed_event(self, event):

        failed_events = []

        if os.path.exists(self.dead_letter_file):

            with open(self.dead_letter_file, "r") as f:

                try:

                    failed_events = json.load(f)

                except:

                    failed_events = []

        failed_events.append(event)

        with open(self.dead_letter_file, "w") as f:

            json.dump(
                failed_events,
                f,
                indent=4
            )

        print("[DEAD LETTER] Event saved.")
