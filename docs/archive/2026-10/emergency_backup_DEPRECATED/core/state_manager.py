import json
import os
from datetime import datetime


class StateManager:

    def __init__(self):

        self.state_file = "data/memory/system_state.json"

        self.default_state = {

            "last_startup": "",
            "last_runtime_save": "",

            "system_status": "IDLE",

            "active_strategy": "default",

            "risk_mode": "NORMAL",

            "confidence_score": 0.0,

            "trading_enabled": True,

            "market_regime": "UNKNOWN",

            "market_message": "No analysis"
        }

    def load_state(self):

        if not os.path.exists(self.state_file):

            self.save_default_state()

        with open(self.state_file, "r") as file:

            state = json.load(file)

        print("[STATE MANAGER] State loaded.")

        return state

    def save_default_state(self):

        os.makedirs("data/memory", exist_ok=True)

        self.default_state["last_startup"] = str(datetime.now())

        with open(self.state_file, "w") as file:

            json.dump(self.default_state, file, indent=4)

        print("[STATE MANAGER] Default state created.")

    def update_state(self, key, value):

        state = self.load_state()

        state[key] = value

        with open(self.state_file, "w") as file:

            json.dump(state, file, indent=4)

        print(f"[STATE MANAGER] Updated: {key} = {value}")

    def save_runtime_state(self):

        state = self.load_state()

        state["last_runtime_save"] = str(datetime.now())

        with open(self.state_file, "w") as file:

            json.dump(state, file, indent=4)

        print("[STATE MANAGER] Runtime state saved.")
