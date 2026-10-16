import os, requests
key = os.getenv('ALPHA_VANTAGE_KEY')
print("Chiave:", key)
if key:
    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=15min&apikey={key}&outputsize=full"
    r = requests.get(url)
    print("Status:", r.status_code)
    print(r.text[:500])
