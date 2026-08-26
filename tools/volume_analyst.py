from datetime import datetime

def get_session():
    hour = datetime.now().hour
    if 8 <= hour < 16:
        return "London", "alta"
    elif 14 <= hour < 22:
        return "New York", "alta"
    else:
        return "Tokyo", "bassa"

def analyze_volume(df):
    if 'Volume' not in df.columns:
        return "normale", 0
    avg = df['Volume'].mean()
    last = df['Volume'].iloc[-1] if len(df) > 0 else 0
    if last > avg * 1.5:
        return "alto", last
    elif last < avg * 0.5:
        return "basso", last
    return "normale", last
