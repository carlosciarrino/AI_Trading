# AI_BRIDGE - Central Risk Engine

class CentralRiskEngine:

    def __init__(self):

        self.max_drawdown = 0.20
        self.max_positions = 10

    # =========================================
    # APPROVAL
    # =========================================

    def approve(self, portfolio):

        if portfolio["drawdown"] > self.max_drawdown:
            return False

        if portfolio["positions"] > self.max_positions:
            return False

        return True
