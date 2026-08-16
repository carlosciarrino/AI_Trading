from core.memory_engine import MemoryEngine
from core.telemetry import Telemetry


class FeedbackEngine:

    def __init__(self):

        self.memory = MemoryEngine()

        self.telemetry = Telemetry()

    def process_trade_feedback(self, performance_report):

        if performance_report is None:

            print("[FEEDBACK] No data available.")

            return

        winrate = performance_report.get("winrate", 0)

        profit_factor = performance_report.get("profit_factor", 0)

        net_profit = performance_report.get("net_profit", 0)

        print("\n[FEEDBACK ENGINE] Processing...\n")

        # POSITIVE LEARNING

        if net_profit > 0 and winrate > 55:

            self.memory.remember_win({

                "winrate": winrate,
                "profit_factor": profit_factor

            })

            self.telemetry.record(

                "learning_event",
                "positive_pattern"

            )

            print("[FEEDBACK] Positive pattern stored.")

        # NEGATIVE LEARNING

        elif net_profit < 0 or winrate < 45:

            self.memory.remember_loss({

                "winrate": winrate,
                "profit_factor": profit_factor

            })

            self.telemetry.record(

                "learning_event",
                "negative_pattern"

            )

            print("[FEEDBACK] Negative pattern stored.")

        else:

            print("[FEEDBACK] Neutral pattern ignored.")
