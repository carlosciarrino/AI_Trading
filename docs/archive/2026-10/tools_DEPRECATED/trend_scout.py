import yfinance as yf

def get_trend(symbol="EURUSD=X", interval="1d", length=50):
    try:
        df = yf.download(symbol, period="60d", interval="1d", multi_level_index=False)
        if df.empty:
            return "neutrale", 0
        sma20 = df['Close'].tail(20).mean()
        sma50 = df['Close'].tail(50).mean()
        if sma20 > sma50:
            return "rialzista", sma20 - sma50
        else:
            return "ribassista", sma20 - sma50
    except:
        return "neutrale", 0
