# AI_BRIDGE - ZeroMQ Event Bus

import zmq
import json


class ZMQBus:

    def __init__(self):

        context = zmq.Context()

        self.publisher = context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:5555")

    # =========================================
    # PUBLISH EVENT
    # =========================================

    def publish(self, topic, data):

        payload = {
            "topic": topic,
            "data": data
        }

        self.publisher.send_string(
            f"{topic} {json.dumps(payload)}"
        )

        print(f"[ZMQ] Published → {topic}")
