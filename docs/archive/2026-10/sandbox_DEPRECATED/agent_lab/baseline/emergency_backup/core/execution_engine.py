from core.confidence_engine import ConfidenceEngine
from core.market_intelligence import MarketIntelligence
from core.mt4_bridge import MT4Bridge
from core.smart_file_sync_engine import SmartFileSyncEngine


class ExecutionEngine:

    def __init__(self):

        self.confidence_engine = ConfidenceEngine()

        self.market_intelligence = MarketIntelligence()

        self.bridge = MT4Bridge()

        self.sync_engine = SmartFileSyncEngine()

    def should_execute_trade(self, performance, state):

        confidence = self.confidence_engine.calculate_confidence(
            performance
        )

        if confidence < 0.60:

            print("[EXECUTION] Blocked: low confidence")

            return False, confidence

        if not state.get("trading_enabled", True):

            print("[EXECUTION] Blocked: system disabled")

            return False, confidence

        if state.get("risk_mode") == "LOCKDOWN":

            print("[EXECUTION] Blocked: lockdown mode")

            return False, confidence

        return True, confidence

    def execute(self, performance, market_data, state):

        allowed, confidence = self.should_execute_trade(
            performance,
            state
        )

        if not allowed:

            return False

        direction = "BUY"

        lot = 0.01

        sl = 20

        tp = 40

        signal = f"{direction},{lot},{sl},{tp}"

        # SCRIVE SEGNALE

        self.bridge.execute_safe_trade(signal)

        # SMART SYNC

        self.sync_engine.full_sync_cycle()

        print("[EXECUTION] Smart sync completed.")

        return True
