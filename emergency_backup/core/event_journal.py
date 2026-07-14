import json
import os
import time


class EventJournal:

    def __init__(self):

        self.journal_file = (
            "data/logs/event_journal.json"
        )

        os.makedirs(
            "data/logs",
            exist_ok=True
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

    def save_event(

        self,
        event_type,
        data

    ):

        events = self.load_events()

        event = {

            "timestamp": time.time(),

            "event_type": event_type,

            "data": data

        }

        events.append(event)

        with open(
            self.journal_file,
            "w"
        ) as f:

            json.dump(
                events,
                f,
                indent=4
            )

        print(

            f"[EVENT JOURNAL] "
            f"Saved: {event_type}"

        )

    def get_recent_events(

        self,
        limit=10

    ):

        events = self.load_events()

        return events[-limit:]

    def print_recent_events(

        self,
        limit=10

    ):

        events = self.get_recent_events(limit)

        print("\n[RECENT EVENTS]\n")

        for event in events:

            print(json.dumps(
                event,
                indent=4
            ))
