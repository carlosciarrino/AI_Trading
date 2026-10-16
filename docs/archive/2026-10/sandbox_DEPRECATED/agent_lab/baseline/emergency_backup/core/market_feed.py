import random


class MarketFeed:

    def get_market_snapshot(self):

        snapshot = {

            "volatility": round(
                random.uniform(0.5, 3.0),
                2
            ),

            "spread": round(
                random.uniform(0.5, 5.0),
                2
            ),

            "trend_strength": round(
                random.uniform(0, 1),
                2
            ),

            "session": random.choice([

                "ASIA",
                "LONDON",
                "NEW_YORK"

            ])
        }

        print("\n[MARKET SNAPSHOT]\n")

        print(snapshot)

        return snapshot
