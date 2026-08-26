from flask import Flask, render_template_string, jsonify, request
import json, os, yfinance as yf
from datetime import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI_BRIDGE Chart</title>
    <style>
        body { background: #0b0e14; color: #e5e9f0; font-family: sans-serif; padding: 20px; }
        .controls { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 20px; background: #131722; padding: 16px; border-radius: 12px; }
        .controls label { color: #78828c; font-size: 13px; display: flex; flex-direction: column; gap: 4px; }
        .controls select, .controls button { background: #1e222d; border: 1px solid #2a2e39; border-radius: 8px; padding: 8px 14px; color: #e5e9f0; font-size: 14px; }
        .controls button { background: #2962ff; cursor: pointer; font-weight: 600; }
        #tradingview_chart { width: 100%; height: 500px; background: #131722; border-radius: 12px; border: 1px solid #2a2e39; }
    </style>
</head>
<body>
    <h1>📈 Trading Chart</h1>
    <div class="controls">
        <label>Simbolo
            <select id="symbol">
                <option value="EURUSD=X">EUR/USD</option>
                <option value="GBPUSD=X">GBP/USD</option>
                <option value="GC=F">Oro</option>
                <option value="^IXIC">NAS100</option>
            </select>
        </label>
        <label>Timeframe
            <select id="interval">
                <option value="1m">1 min</option>
                <option value="5m">5 min</option>
                <option value="15m">15 min</option>
                <option value="1h">1 ora</option>
                <option value="4h">4 ore</option>
                <option value="1d" selected>Daily</option>
            </select>
        </label>
        <label>Periodo
            <select id="period">
                <option value="30d" selected>1 mese</option>
                <option value="90d">3 mesi</option>
                <option value="180d">6 mesi</option>
                <option value="1y">1 anno</option>
            </select>
        </label>
        <button onclick="alert('Il grafico TradingView è in tempo reale e si aggiorna automaticamente.')">Aggiorna</button>
    </div>
    <div id="tradingview_chart"></div>
    <!-- TradingView Widget BEGIN -->
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({
        "autosize": true,
        "symbol": "FX:EURUSD",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "it",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_chart"
    });
    </script>
    <!-- TradingView Widget END -->
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/chart_data', methods=['POST'])
def chart_data():
    data = request.json
    symbol = data.get('symbol', 'EURUSD=X')
    period = data.get('period', '30d')
    interval = data.get('interval', '1d')
    try:
        df = yf.download(symbol, period=period, interval=interval, multi_level_index=False)
        if df.empty:
            return jsonify({'error': 'Nessun dato'})
        df = df[['Open','High','Low','Close']].tail(100)
        df = df.reset_index()
        records = df.to_dict(orient='records')
        for r in records:
            if 'Date' in r:
                r['Date'] = r['Date'].strftime('%Y-%m-%d')
        return jsonify(records)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
