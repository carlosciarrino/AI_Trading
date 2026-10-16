class ConfidenceEngine:

    def __init__(self):

        self.minimum_confidence = 0.60

    def calculate_confidence(self, performance):

        if performance is None:

            return 0.0

        confidence = 0.0

        winrate = performance.get("winrate", 0)

        profit_factor = performance.get("profit_factor", 0)

        average_profit = performance.get("average_profit", 0)

        trade_count = performance.get("trade_count", 0)

        # WINRATE WEIGHT

        confidence += (winrate / 100) * 0.4

        # PROFIT FACTOR WEIGHT

        confidence += min(profit_factor / 3, 1) * 0.4

        # AVERAGE PROFIT WEIGHT

        confidence += min(max(average_profit / 10, 0), 1) * 0.1

        # TRADE SAMPLE SIZE BONUS

        if trade_count >= 20:

            confidence += 0.1

        confidence = round(confidence, 2)

        print(f"\n[CONFIDENCE SCORE] {confidence}\n")

        return confidence

    def is_safe_to_trade(self, confidence):

        if confidence >= self.minimum_confidence:

            print("[CONFIDENCE] Trading ENABLED.")

            return True

        print("[CONFIDENCE] Trading BLOCKED.")

        return False
