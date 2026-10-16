from core.runtime_controller import (
    RuntimeController
)

from core.event_bus import (
    EventBus
)


class AutonomicResponseEngine:

    def __init__(self):

        self.runtime = RuntimeController()

        self.bus = EventBus()

    def process_anomaly(

        self,
        anomaly_type,
        data=None

    ):

        print(

            f"\n[AUTONOMIC RESPONSE] "
            f"{anomaly_type}\n"

        )

        # EVENT SPAM

        if anomaly_type == "event_spam":

            self.handle_event_spam(data)

        # RISK ALERT

        elif anomaly_type == "risk_alert":

            self.handle_risk_alert(data)

        # FAILURE PATTERN

        elif anomaly_type == "failure_pattern":

            self.handle_failure_pattern(data)

        # OVERLOAD

        elif anomaly_type == "runtime_overload":

            self.handle_runtime_overload(data)

        else:

            print(

                "[AUTONOMIC RESPONSE] "
                "Unknown anomaly."

            )

    def handle_event_spam(

        self,
        data

    ):

        print(

            "[ACTION] "
            "Activating SAFE MODE."

        )

        self.runtime.enable_safe_mode()

        self.bus.publish(

            "safe_mode_activated",

            {

                "reason": "event_spam"

            }

        )

    def handle_risk_alert(

        self,
        data

    ):

        drawdown = data.get(
            "drawdown",
            0
        )

        print(

            f"[ACTION] "
            f"Drawdown detected: {drawdown}"

        )

        if drawdown >= 15:

            print(

                "[ACTION] "
                "Trading disabled."

            )

            self.runtime.enable_safe_mode()

            self.bus.publish(

                "trading_blocked",

                {

                    "reason": "high_drawdown"

                }

            )

    def handle_failure_pattern(

        self,
        data

    ):

        module = data.get(
            "module",
            "unknown"
        )

        print(

            f"[ACTION] "
            f"Failure in module: {module}"

        )

        self.runtime.start_recovery_mode()

        self.bus.publish(

            "recovery_started",

            {

                "module": module

            }

        )

    def handle_runtime_overload(

        self,
        data

    ):

        print(

            "[ACTION] "
            "Runtime overload detected."

        )

        self.runtime.enable_safe_mode()

        self.bus.publish(

            "runtime_throttled",

            {

                "reason": "overload"

            }

        )
