class RiskMode:

    def detect_mode(self, performance):

        if performance is None:

            return "LOCKDOWN"

        winrate = performance.get("winrate", 0)

        profit_factor = performance.get("profit_factor", 0)

        if winrate < 40:

            return "SURVIVAL"

        if profit_factor < 1:

            return "DEFENSIVE"

        if winrate > 60 and profit_factor > 1.5:

            return "AGGRESSIVE"

        return "NORMAL"
