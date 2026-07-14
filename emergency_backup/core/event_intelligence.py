import json
import os
from collections import Counter


class EventIntelligence:

    def __init__(self):

        self.journal_file = (
            "data/logs/event_journal.json"
        )

    def load_events(self):

        if not os.path.exists(
            self.journal_file
        ):

            return []

        with open(
            self.journal_file,
            "r"
        ) as f:

            try:

                return json.load(f)

            except:

                return []

    def analyze_events(self):

        events = self.load_events()

        if not events:

            print(
                "[EVENT INTELLIGENCE] "
                "No events found."
            )

            return

        event_types = [

            event["event_type"]

            for event in events

        ]

        counts = Counter(event_types)

        print("\n[EVENT ANALYSIS]\n")

        print(

            f"TOTAL EVENTS: "
            f"{len(events)}\n"

        )

        print("EVENT FREQUENCY:\n")

        for event_type, count in counts.items():

            print(f"{event_type}: {count}")

        self.detect_anomalies(counts)

    def detect_anomalies(

        self,
        counts

    ):

        print("\n[ANOMALY DETECTION]\n")

        anomalies_found = False

        for event_type, count in counts.items():

            # EVENT SPAM

            if count >= 10:

                print(

                    f"[WARNING] "
                    f"High frequency event: "
                    f"{event_type}"

                )

                anomalies_found = True

            # RISK EVENTS

            if "risk" in event_type:

                print(

                    f"[RISK EVENT DETECTED] "
                    f"{event_type}"

                )

                anomalies_found = True

            # FAILURE EVENTS

            if "failure" in event_type:

                print(

                    f"[FAILURE PATTERN] "
                    f"{event_type}"

                )

                anomalies_found = True

        if not anomalies_found:

            print(

                "[EVENT INTELLIGENCE] "
                "No anomalies detected."

            )

