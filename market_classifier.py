def classify_market(volatility, trend):

    if volatility > 0.8:
        return "EXPLOSIVE"

    if trend > 0.7:
        return "TRENDING"

    if volatility < 0.3:
        return "RANGING"

    return "NORMAL"
