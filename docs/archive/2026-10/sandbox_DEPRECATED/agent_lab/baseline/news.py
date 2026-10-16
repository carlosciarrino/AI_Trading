import random

def get_news_sentiment():
    r = random.randint(1, 10)

    if r <= 3:
        return "BUY"
    elif r >= 8:
        return "SELL"
    else:
        return "NONE"
