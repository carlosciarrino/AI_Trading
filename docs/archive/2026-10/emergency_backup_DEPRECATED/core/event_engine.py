import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from core.event_filter_engine import EventFilterEngine
from core.event_queue_engine import EventQueueEngine


class AIEventHandler(FileSystemEventHandler):

    def __init__(self):

        self.filter_engine = EventFilterEngine()

        self.queue_engine = EventQueueEngine()

        self.queue_engine.start_worker()

    def on_modified(self, event):

        if event.is_directory:

            return

        path = event.src_path

        if not self.filter_engine.should_process(path):

            return

        print(f"[EVENT ACCEPTED] {path}")

        # PRIORITÀ EVENTI

        priority = 5

        if "ai_confirm" in path:

            priority = 1

        elif "mt4_trades_snapshot" in path:

            priority = 2

        elif "ai_signal" in path:

            priority = 3

        self.queue_engine.add_event(

            priority,
            "file_modified",
            path

        )


class EventEngine:

    def __init__(self, watch_path):

        self.watch_path = watch_path

        self.observer = Observer()

    def start(self):

        event_handler = AIEventHandler()

        self.observer.schedule(
            event_handler,
            self.watch_path,
            recursive=False
        )

        self.observer.start()

        print(f"[EVENT ENGINE] Watching: {self.watch_path}")

    def run_forever(self):

        try:

            while True:

                time.sleep(1)

        except KeyboardInterrupt:

            self.observer.stop()

        self.observer.join()
