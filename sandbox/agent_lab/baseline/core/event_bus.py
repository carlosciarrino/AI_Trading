# AI_BRIDGE - Institutional Event Bus

import json
import time
from datetime import datetime
from collections import deque


class EventBus:
    """
    Sistema centrale di comunicazione asincrona.
    """

    def __init__(self):

        self.queue = deque()
        self.subscribers = []

    # =========================================
    # PUBLISH EVENT
    # =========================================

    def publish(self, event_type, data):

        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.queue.append(event)

        print(f"[EVENT_BUS] PUBLISHED → {event_type}")

    # =========================================
    # SUBSCRIBE
    # =========================================

    def subscribe(self, handler):

        self.subscribers.append(handler)

    # =========================================
    # DISPATCH LOOP
    # =========================================

    def dispatch(self):

        while self.queue:

            event = self.queue.popleft()

            for handler in self.subscribers:
                handler(event)
