from datetime import datetime
import json
import os


class Telemetry:

    def __init__(self):

        self.telemetry_file = "data/logs/telemetry.json"

    def record(self, event, value):

        os.makedirs("data/logs", exist_ok=True)

        entry = {

            "timestamp": str(datetime.now()),
            "event": event,
            "value": value

        }

        data = []

        if os.path.exists(self.telemetry_file):

            with open(self.telemetry_file, "r") as file:

                try:
                    data = json.load(file)
                except:
                    data = []

        data.append(entry)

        with open(self.telemetry_file, "w") as file:

            json.dump(data, file, indent=4)

        print(f"[TELEMETRY] Event recorded: {event}")
