import json
import os

LOG_FILE = "trades_log.txt"
STATS_FILE = "stats.json"


def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"BUY": [], "SELL": []}

    with open(STATS_FILE, "r") as f:
        return json.load(f)


def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)


def parse_trade_block(block):
    data = {}
    for line in block:
        if "=" in line:
            k, v = line.split("=")
            data[k.strip()] = v.strip()
    return data


def evaluate_trade(trade):
    pips = float(trade.get("pips", 0))
    ttype = trade.get("type", "UNKNOWN")

    if ttype not in ["BUY", "SELL"]:
        return None

    return {
        "type": ttype,
        "pips": pips,
        "good": pips > 0
    }


def update_learning():
    if not os.path.exists(LOG_FILE):
        return

    with open(LOG_FILE, "r") as f:
        lines = f.read().strip().split("\n")

    stats = load_stats()

    block = []
    for line in lines:
        if line.strip() == "":
            continue
        block.append(line)

        if len(block) == 6:  # trade completo
            trade = parse_trade_block(block)
            result = evaluate_trade(trade)

            if result:
                stats[result["type"]].append(result["pips"])

            block = []

    save_stats(stats)


def get_signal_bias():
    stats = load_stats()

    def avg(lst):
        return sum(lst) / len(lst) if lst else 0

    buy_score = avg(stats.get("BUY", []))
    sell_score = avg(stats.get("SELL", []))

    if buy_score > sell_score:
        return "BUY_BIAS"
    elif sell_score > buy_score:
        return "SELL_BIAS"
    else:
        return "NEUTRAL"


if __name__ == "__main__":
    update_learning()
