class ValidationEngine:

    def __init__(self):

        self.rules = {

            "ema_fast_min": 5,
            "ema_fast_max": 100,

            "stop_loss_min": 5,
            "stop_loss_max": 100,

            "take_profit_min": 5,
            "take_profit_max": 300,

            "confidence_min": 0.50,
            "confidence_max": 0.95,

            "risk_min": 0.1,
            "risk_max": 5.0
        }

    def validate_strategy(self, strategy):

        errors = []

        if not (
            self.rules["ema_fast_min"]
            <= strategy["ema_fast"]
            <= self.rules["ema_fast_max"]
        ):

            errors.append("EMA_FAST_OUT_OF_RANGE")

        if not (
            self.rules["stop_loss_min"]
            <= strategy["stop_loss"]
            <= self.rules["stop_loss_max"]
        ):

            errors.append("STOP_LOSS_OUT_OF_RANGE")

        if not (
            self.rules["take_profit_min"]
            <= strategy["take_profit"]
            <= self.rules["take_profit_max"]
        ):

            errors.append("TAKE_PROFIT_OUT_OF_RANGE")

        if not (
            self.rules["confidence_min"]
            <= strategy["confidence_threshold"]
            <= self.rules["confidence_max"]
        ):

            errors.append("CONFIDENCE_OUT_OF_RANGE")

        if not (
            self.rules["risk_min"]
            <= strategy["risk_per_trade"]
            <= self.rules["risk_max"]
        ):

            errors.append("RISK_OUT_OF_RANGE")

        if strategy["take_profit"] <= strategy["stop_loss"]:

            errors.append("BAD_RISK_REWARD_RATIO")

        if errors:

            return False, errors

        return True, []
