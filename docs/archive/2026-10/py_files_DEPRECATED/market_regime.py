import pandas as pd

def detect_market_regime(df):

    volatility = df['close'].pct_change().std()

    trend = abs(df['close'].iloc[-1] - df['close'].mean())

    if volatility > 0.003:
        return "HIGH_VOLATILITY"

    if trend > 0.002:
        return "TRENDING"

    return "RANGING"
