import pandas as pd

def optimize():

    try:
        df = pd.read_csv("trades_log.txt")

        wins = df[df["profit"] > 0]
        losses = df[df["profit"] <= 0]

        winrate = len(wins) / len(df)

        if winrate < 0.45:
            return {
                "risk": 0.5,
                "mode": "SAFE"
            }

        if winrate > 0.65:
            return {
                "risk": 2.0,
                "mode": "AGGRESSIVE"
            }

        return {
            "risk": 1.0,
            "mode": "NORMAL"
        }

    except:
        return {
            "risk": 1.0,
            "mode": "NORMAL"
        }
