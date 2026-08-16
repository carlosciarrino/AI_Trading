import json
import os


class StrategyManager:

    def __init__(self):

        self.strategy_file = "data/memory/active_strategy.json"

        self.default_strategy = {

            "name": "baseline_strategy",

            "ema_fast": 21,
            "ema_slow": 50,

            "stop_loss": 20,
            "take_profit": 40,

            "confidence_threshold": 0.70,

            "risk_per_trade": 1.0
        }

        self.load_strategy()

    def load_strategy(self):

        if not os.path.exists(self.strategy_file):

            self.save_strategy(self.default_strategy)

        with open(self.strategy_file, "r") as file:

            strategy = json.load(file)

        print("[STRATEGY] Active strategy loaded.")

        return strategy

    def save_strategy(self, strategy):

        os.makedirs("data/memory", exist_ok=True)

        with open(self.strategy_file, "w") as file:

            json.dump(strategy, file, indent=4)

        print("[STRATEGY] Strategy saved.")
