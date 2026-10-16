import pandas as pd

def load_trades(file_path="trades_log.txt"):
    df = pd.read_csv(file_path, sep=",")

    # pulizia nomi colonne (IMPORTANTISSIMO)
    df.columns = df.columns.str.strip()

    return df


def stats():
    df = load_trades()

    # debug utile (puoi lasciarlo o togliere dopo)
    print("COLONNE LETTE:", df.columns.tolist())

    if "profit" not in df.columns:
        raise Exception("Colonna 'profit' non trovata nel file trades_log.txt")

    wins = len(df[df["profit"] > 0])
    losses = len(df[df["profit"] <= 0])

    total = len(df)

    winrate = (wins / total) * 100 if total > 0 else 0

    return {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "winrate": round(winrate, 2)
    }
