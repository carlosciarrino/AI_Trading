class MarketRegime:

    def detect_regime(self, market_data):

        """
        market_data example:

        {
            "volatility": 1.2,
            "spread": 1.5,
            "trend_strength": 0.8,
            "session": "LONDON"
        }
        """

        volatility = market_data.get("volatility", 0)

        spread = market_data.get("spread", 0)

        trend_strength = market_data.get(
            "trend_strength",
            0
        )

        session = market_data.get("session", "UNKNOWN")

        regime = "UNKNOWN"

        # TOXIC MARKET

        if spread > 4:

            regime = "TOXIC"

        # HIGH VOLATILITY

        elif volatility > 2:

            regime = "VOLATILE"

        # STRONG TREND

        elif trend_strength > 0.7:

            regime = "TRENDING"

        # SIDEWAYS

        elif trend_strength < 0.3:

            regime = "RANGING"

        else:

            regime = "NORMAL"

        print(f"\n[MARKET REGIME] {regime}")

        return {

            "regime": regime,
            "session": session,
            "volatility": volatility,
            "spread": spread,
            "trend_strength": trend_strength
        }
