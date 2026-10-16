import time


class EventFilterEngine:

    def __init__(self):

        self.last_events = {}

        self.cooldown_seconds = 2

    def is_duplicate(self, path):

        now = time.time()

        last_time = self.last_events.get(path, 0)

        # debounce anti spam

        if now - last_time < self.cooldown_seconds:

            print(f"[EVENT FILTER] Ignored duplicate: {path}")

            return True

        self.last_events[path] = now

        return False

    def should_process(self, path):

        if path.endswith(".tmp"):

            print(f"[EVENT FILTER] Ignored temp file: {path}")

            return False

        if self.is_duplicate(path):

            return False

        return True
