from core.runtime_controller import (
    RuntimeController
)


class RiskGovernor:

    def __init__(self):

        self.runtime = RuntimeController()

        self.max_drawdown = 15

        self.min_confidence = 0.60

    def can_trade(

        self,
        confidence,
        drawdown

    ):

        state = self.runtime.load_state()

        # SAFE MODE

        if state["safe_mode"]:

            print(
                "[RISK GOVERNOR] "
                "Trading blocked: SAFE MODE"
            )

            return False

        # EVOLUTION MODE

        if state["evolution_mode"]:

            print(
                "[RISK GOVERNOR] "
                "Trading blocked: EVOLUTION MODE"
            )

            return False

        # RECOVERY MODE

        if state["recovery_mode"]:

            print(
                "[RISK GOVERNOR] "
                "Trading blocked: RECOVERY MODE"
            )

            return False

        # DRAWNDOWN CHECK

        if drawdown >= self.max_drawdown:

            print(
                "[RISK GOVERNOR] "
                "Drawdown exceeded."
            )

            self.runtime.enable_safe_mode()

            return False

        # CONFIDENCE CHECK

        if confidence < self.min_confidence:

            print(
                "[RISK GOVERNOR] "
                "Confidence too low."
            )

            return False

        print(
            "[RISK GOVERNOR] "
            "Trade approved."
        )

        return True

    def can_evolve(self):

        state = self.runtime.load_state()

        # SAFE MODE BLOCK

        if state["safe_mode"]:

            print(
                "[RISK GOVERNOR] "
                "Evolution blocked: SAFE MODE"
            )

            return False

        # RECOVERY BLOCK

        if state["recovery_mode"]:

            print(
                "[RISK GOVERNOR] "
                "Evolution blocked: RECOVERY MODE"
            )

            return False

        return True
