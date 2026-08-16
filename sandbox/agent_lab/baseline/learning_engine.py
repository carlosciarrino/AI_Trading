import pandas as pd

FILE = "market_memory.csv"
ANTI_FILE = "anti_memory.csv"


def load(file):
    try:
        return pd.read_csv(file)
    except:
        return pd.DataFrame()


def save_trade(data):
    df = load(FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(FILE, index=False)


def save_loss(data):
    df = load(ANTI_FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(ANTI_FILE, index=False)


def adjust_weights():

    df_win = load(FILE)
    df_loss = load(ANTI_FILE)

    if len(df_win) < 20:
        return {
            "trend": 30,
            "volatility": 20,
            "momentum": 20,
            "news": 15,
            "ai": 10
        }

    # pattern vincenti
    win_bias = df_win.mean(numeric_only=True)

    # pattern perdenti
    loss_bias = df_loss.mean(numeric_only=True)

    trend = 30 + (win_bias.get("trend", 0) - loss_bias.get("trend", 0)) * 10
    vol = 20 + (win_bias.get("volatility", 0) - loss_bias.get("volatility", 0)) * 10
    mom = 20 + (win_bias.get("momentum", 0) - loss_bias.get("momentum", 0)) * 10

    return {
        "trend": max(5, trend),
        "volatility": max(5, vol),
        "momentum": max(5, mom),
        "news": 15,
        "ai": 10
    }
