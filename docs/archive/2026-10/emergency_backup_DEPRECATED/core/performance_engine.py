import csv
import os


class PerformanceEngine:

    def __init__(self):

        self.trades_file = "data/trades/trades_log.txt"

    def analyze(self):

        if not os.path.exists(self.trades_file):

            print("[PERFORMANCE] No trades log found.")

            return None

        profits = []

        wins = 0

        losses = 0

        total_profit = 0

        total_loss = 0

        trade_count = 0

        with open(self.trades_file, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                try:

                    profit = float(row["profit"])

                    profits.append(profit)

                    trade_count += 1

                    if profit > 0:

                        wins += 1

                        total_profit += profit

                    else:

                        losses += 1

                        total_loss += abs(profit)

                except:

                    continue

        if trade_count == 0:

            print("[PERFORMANCE] No valid trades.")

            return None

        winrate = (wins / trade_count) * 100

        profit_factor = (
            total_profit / total_loss
            if total_loss > 0
            else total_profit
        )

        net_profit = sum(profits)

        average_profit = net_profit / trade_count

        performance = {

            "trade_count": trade_count,
            "wins": wins,
            "losses": losses,
            "winrate": round(winrate, 2),
            "profit_factor": round(profit_factor, 2),
            "net_profit": round(net_profit, 2),
            "average_profit": round(average_profit, 2)

        }

        print("\n[PERFORMANCE REPORT]\n")

        for key, value in performance.items():

            print(f"{key}: {value}")

        return performance
