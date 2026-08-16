import json
import os
import threading
import time


class RuntimeController:

    def __init__(self):

        self.runtime_file = (
            "data/runtime_state.json"
        )

        self.lock = threading.Lock()

        self.default_state = {

            "system_status": "STARTING",

            "trading_enabled": True,

            "safe_mode": False,

            "evolution_mode": False,

            "recovery_mode": False,

            "last_update": time.time()

        }

        self.initialize_runtime()

    def initialize_runtime(self):

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.runtime_file):

            self.save_state(self.default_state)

    def load_state(self):

        with self.lock:

            try:

                with open(self.runtime_file, "r") as f:

                    return json.load(f)

            except:

                return self.default_state.copy()

    def save_state(self, state):

        with self.lock:

            state["last_update"] = time.time()

            with open(self.runtime_file, "w") as f:

                json.dump(state, f, indent=4)

    def update_state(self, key, value):

        state = self.load_state()

        state[key] = value

        self.save_state(state)

        print(f"[RUNTIME] {key} -> {value}")

    def set_system_status(self, status):

        allowed = [

            "STARTING",
            "RUNNING",
            "SAFE_MODE",
            "EVOLVING",
            "RECOVERING",
            "SHUTDOWN"

        ]

        if status not in allowed:

            print("[RUNTIME] Invalid status")

            return

        self.update_state(
            "system_status",
            status
        )

    def enable_safe_mode(self):

        self.update_state(
            "safe_mode",
            True
        )

        self.update_state(
            "trading_enabled",
            False
        )

        self.set_system_status(
            "SAFE_MODE"
        )

    def disable_safe_mode(self):

        self.update_state(
            "safe_mode",
            False
        )

        self.update_state(
            "trading_enabled",
            True
        )

        self.set_system_status(
            "RUNNING"
        )

    def start_evolution_mode(self):

        self.update_state(
            "evolution_mode",
            True
        )

        self.set_system_status(
            "EVOLVING"
        )

    def stop_evolution_mode(self):

        self.update_state(
            "evolution_mode",
            False
        )

        self.set_system_status(
            "RUNNING"
        )

    def start_recovery_mode(self):

        self.update_state(
            "recovery_mode",
            True
        )

        self.set_system_status(
            "RECOVERING"
        )

    def stop_recovery_mode(self):

        self.update_state(
            "recovery_mode",
            False
        )

        self.set_system_status(
            "RUNNING"
        )

    def shutdown_system(self):

        self.update_state(
            "trading_enabled",
            False
        )

        self.set_system_status(
            "SHUTDOWN"
        )

    def get_runtime_summary(self):

        state = self.load_state()

        print("\n[RUNTIME STATUS]\n")

        print(json.dumps(state, indent=4))

        return state
