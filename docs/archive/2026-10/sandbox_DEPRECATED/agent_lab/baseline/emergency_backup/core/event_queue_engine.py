import queue
import time
import threading

from core.retry_engine import RetryEngine
from core.dead_letter_engine import DeadLetterEngine


class EventQueueEngine:

    def __init__(self):

        self.event_queue = queue.PriorityQueue()

        self.running = True

        self.retry_engine = RetryEngine()

        self.dead_letter = DeadLetterEngine()

    def add_event(self, priority, event_type, path):

        event = (

            priority,

            {

                "type": event_type,

                "path": path,

                "timestamp": time.time()

            }

        )

        self.event_queue.put(event)

        print(f"[QUEUE] Added: {event_type}")

    def process_event_logic(self, event):

        print("\n[PROCESSING EVENT]\n")

        print(event)

        # TEST FAILURE SIMULATION

        if "fail" in event["path"]:

            raise Exception("Simulated failure")

    def process_event(self, event):

        success = self.retry_engine.execute_with_retry(

            self.process_event_logic,
            event

        )

        if not success:

            self.dead_letter.save_failed_event(event)

    def worker_loop(self):

        while self.running:

            try:

                priority, event = self.event_queue.get(timeout=1)

                self.process_event(event)

                self.event_queue.task_done()

            except queue.Empty:

                continue

    def start_worker(self):

        thread = threading.Thread(
            target=self.worker_loop,
            daemon=True
        )

        thread.start()

        print("[QUEUE] Worker started.")
