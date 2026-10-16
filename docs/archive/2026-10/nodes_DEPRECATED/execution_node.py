# AI_BRIDGE - Execution Node

import zmq
import json


class ExecutionNode:

    def __init__(self):

        context = zmq.Context()

        self.subscriber = context.socket(zmq.SUB)
        self.subscriber.connect("tcp://localhost:5555")

        self.subscriber.setsockopt_string(
            zmq.SUBSCRIBE,
            "TRADE"
        )

    # =========================================
    # LISTEN LOOP
    # =========================================

    def listen(self):

        while True:

            raw = self.subscriber.recv_string()

            topic, payload = raw.split(" ", 1)

            event = json.loads(payload)

            self.execute(event["data"])

    # =========================================
    # EXECUTION
    # =========================================

    def execute(self, trade):

        print(f"[EXEC NODE] EXECUTING → {trade}")
