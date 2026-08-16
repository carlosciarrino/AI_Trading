import pandas as pd
import json
import os

WEIGHTS_FILE = "weights.json"
TRADES_FILE = "trades_log.txt"


# ---------------------------
# 1. CARICA PESI
# ---------------------------
def load_weights():
    if os.path.exists(WEIGHTS_FILE):
        with open(WEIGHTS_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "trend": 30,
            "volatility": 20,
            "momentum": 20,
            "news": 15,
            "ai_confidence": 10,
            "session": 5
        }


# ---------------------------
# 2. SALVA PESI
# ---------------------------
def save_weights(weights):
    with open(WEIGHTS_FILE, "w") as f:
        json.dump(weights, f, indent=4)


# ---------------------------
# 3. CALCOLO SCORE ADATTIVO
# ---------------------------
def calculate_score(features, weights):
    score = 0

    score += features["trend"] * weights["trend"]
    score += features["volatility"] * weights["volatility"]
    score += features["momentum"] * weights["momentum"]
    score += (1 - features["news"]) * weights["news"]
    score += features["ai_confidence"] * weights["ai_confidence"]
    score += features["session"] * weights["session"]

    return score


# ---------------------------
# 4. APPRENDIMENTO (CUORE DEL SISTEMA)
# ---------------------------
def update_weights():
    df = pd.read_csv(TRADES_FILE)
    df.columns = df.columns.str.strip()

    weights = load_weights()

    # inizializziamo contributi
    contributions = {k: 0 for k in weights.keys()}
    total_profit = 0

    for _, row in df.iterrows():
        profit = row["profit"]
        total_profit += profit

        # normalizzazione semplice
        factor = 1 if profit > 0 else -1

        contributions["trend"] += factor
        contributions["volatility"] += factor
        contributions["momentum"] += factor
        contributions["news"] += factor
        contributions["ai_confidence"] += factor
        contributions["session"] += factor

    # aggiornamento pesi (soft learning)
    for key in weights:
        weights[key] += contributions[key] * 0.1

        # clamp per evitare esplosioni
        weights[key] = max(1, min(weights[key], 100))

    save_weights(weights)

    return weights
