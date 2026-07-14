import json
import os
from collections import Counter


class FailureAnalysisEngine:

    def __init__(self):

        self.dead_letter_file = (
            "data/logs/dead_letter_queue.json"
        )

        self.report_file = (
            "data/logs/failure_report.json"
        )

    def load_failed_events(self):

        if not os.path.exists(self.dead_letter_file):

            return []

        with open(self.dead_letter_file, "r") as f:

            try:

                return json.load(f)

            except:

                return []

    def classify_failure(self, event):

        path = event.get("path", "")

        if "ai_confirm" in path:

            return "CONFIRMATION_FAILURE"

        elif "snapshot" in path:

            return "SNAPSHOT_FAILURE"

        elif "signal" in path:

            return "SIGNAL_FAILURE"

        elif "fail" in path:

            return "SIMULATED_FAILURE"

        return "UNKNOWN_FAILURE"

    def analyze_failures(self):

        failed_events = self.load_failed_events()

        classifications = []

        for event in failed_events:

            category = self.classify_failure(event)

            classifications.append(category)

        stats = Counter(classifications)

        report = {

            "total_failures": len(failed_events),

            "failure_categories": dict(stats)

        }

        with open(self.report_file, "w") as f:

            json.dump(report, f, indent=4)

        print("\n[FAILURE ANALYSIS REPORT]\n")

        print(json.dumps(report, indent=4))

        return report
