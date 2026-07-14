class MarketIntelligence:

    def evaluate_market(self, regime_data):

        regime = regime_data["regime"]

        if regime == "TOXIC":

            return {

                "trade_allowed": False,
                "risk_modifier": 0.0,
                "message": "Market toxic"
            }

        elif regime == "VOLATILE":

            return {

                "trade_allowed": True,
                "risk_modifier": 0.5,
                "message": "High volatility"
            }

        elif regime == "TRENDING":

            return {

                "trade_allowed": True,
                "risk_modifier": 1.2,
                "message": "Strong trend"
            }

        elif regime == "RANGING":

            return {

                "trade_allowed": True,
                "risk_modifier": 0.7,
                "message": "Range market"
            }

        return {

            "trade_allowed": True,
            "risk_modifier": 1.0,
            "message": "Normal market"
        }
