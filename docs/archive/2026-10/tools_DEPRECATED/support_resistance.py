import pandas as pd
import numpy as np

def find_sr(df, window=20, tolerance=0.002):
    highs = df['High'].rolling(window, center=True).max()
    lows = df['Low'].rolling(window, center=True).min()
    levels = []
    for i in range(window, len(df) - window):
        if df['High'].iloc[i] == highs.iloc[i]:
            levels.append(df['High'].iloc[i])
        if df['Low'].iloc[i] == lows.iloc[i]:
            levels.append(df['Low'].iloc[i])
    levels = sorted(set(levels))
    grouped = []
    for l in levels:
        if not grouped or abs(l - grouped[-1]) > tolerance:
            grouped.append(l)
    return grouped
