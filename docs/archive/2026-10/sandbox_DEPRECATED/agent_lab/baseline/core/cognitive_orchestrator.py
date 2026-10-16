# AI_BRIDGE - Distributed Orchestrator

from core.zmq_bus import ZMQBus
from core.central_risk_engine import CentralRiskEngine


class CognitiveOrchestrator:

    def __init__(self):

        self.bus = ZMQBus()
        self.risk = CentralRiskEngine()

    # =========================================
    # MAIN ENTRY
    # =========================================

    def request_action(self, signal):

        portfolio = {
            "drawdown": 0.05,
            "positions": 2
        }

        approved = self.risk.approve(portfolio)

        if not approved:

            print("[RISK] BLOCKED")
            return

        self.bus.publish(
            "TRADE",
            signal
        )

        print("[ORCHESTRATOR] SIGNAL DISPATCHED")
