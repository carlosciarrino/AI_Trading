import pandas as pd
import os

FILE = "market_memory.csv"

def save_trade(data):

    df = pd.DataFrame([data])

    if not os.path.exists(FILE):
        df.to_csv(FILE, index=False)
    else:
        df.to_csv(FILE, mode='a', header=False, index=False)
