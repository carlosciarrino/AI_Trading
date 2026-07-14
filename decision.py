from learning_engine import adjust_weights

def calculate_score(
    trend_strength,
    volatility_level,
    momentum_strength,
    news_impact,
    ai_confidence,
    market_session,
    weights
):

    score = 0

    score += trend_strength * weights["trend"]
    score += volatility_level * weights["volatility"]
    score += momentum_strength * weights["momentum"]
    score += (1 - news_impact) * weights["news"]
    score += ai_confidence * weights["ai"]

    if market_session in ["London", "NewYork"]:
        score += 5

    return round(score, 2)


def trading_decision(score):

    if score >= 80:
        return "AGGRESSIVE BUY"

    elif score >= 65:
        return "BUY"

    elif score >= 45:
        return "WAIT"

    return "NO TRADE"
