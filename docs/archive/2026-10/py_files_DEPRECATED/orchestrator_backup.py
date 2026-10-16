import sys, json, time, logging, os, requests
from datetime import datetime
from core.mt4_bridge import MT4Bridge
from tools.live_data import get_recent
from tools.live_data import get_recent_yahoo
from tools.live_data import get_recent_yahoo
from tools.live_data import get_recent_yahoo
from tools.risk_manager import RiskManager
from tools.portfolio_manager import PortfolioManager
from tools.support_resistance import find_sr
from tools.news_fetcher import get_forex_live_news, analyze_sentiment
from tools.x_sentiment import get_tweets, analyze_sentiment as analyze_x
from tools.volume_analyst import get_session, analyze_volume
from tools.trend_scout import get_trend
from prompts import prompt_bull, prompt_bear, prompt_judge

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class TradingOrchestrator:
    def __init__(self):
        with open('mt4_bridge_config.json', 'r') as f:
            config = json.load(f)
        self.bridge = MT4Bridge(config=config)
        self.risk = RiskManager()
        self.pm = PortfolioManager()
        logger.info("Orchestrator multi-agente init OK")

    def ask_ollama(self, prompt):
        try:
            resp = requests.post("http://localhost:11434/api/generate",
                                 json={"model": "llama3.2:3b", "prompt": prompt, "stream": False},
                                 timeout=120)
            if resp.status_code != 200:
                return ""
            return resp.json().get("response", "")
        except:
            return ""

    def get_ai_signal(self, symbol="EUR/USD"):
        try:
            with open('config.json') as f:
                cfg = json.load(f)
            interval = cfg.get('timeframe', '15min')
    try:
        df = get_recent(symbol, interval=interval, length=50)
    except:
        df = get_recent_yahoo(symbol, interval=interval, length=50)

            # 1. Supporti/Resistenze
            levels = find_sr(df)
            sr_info = f"SR: {', '.join([f'{l:.5f}' for l in levels])}"

            # 2. Notizie ForexLive
            news = get_forex_live_news(3)
            sentiment_news = analyze_sentiment(news)

            # 3. Sentiment X
            tweets = get_tweets(limit=3)
            sentiment_x = analyze_x(tweets)

            # 4. Volumi e fuso orario
            session, liquidity = get_session()
            vol_status, vol_value = analyze_volume(df)

            # 5. Trend scout su H1 e H4
            trend_h1, _ = get_trend(symbol, "1h", 50)
            trend_h4, _ = get_trend(symbol, "4h", 50)

            # 6. Costruisci contesto per AI
            data_str = f"""
{df.tail(10).to_string()}

📊 Supporti/Resistenze: {sr_info}
📰 News Sentiment: {sentiment_news}
🐦 X Sentiment: {sentiment_x}
⏰ Sessione: {session} (liquidità {liquidity})
📈 Volume: {vol_status} ({vol_value:.0f})
📈 Trend H1: {trend_h1}
📈 Trend H4: {trend_h4}
"""

            bull_response = self.ask_ollama(prompt_bull.format(data_str))
            bear_response = self.ask_ollama(prompt_bear.format(data_str))
            judge_response = self.ask_ollama(prompt_judge.format(bull_response, bear_response))

            final_signal = "HOLD"
            for word in ["BUY", "SELL", "HOLD"]:
                if word in judge_response.upper():
                    final_signal = word
                    break

            # Filtra con supporti/resistenze
            price = df["Close"].iloc[-1]
            if final_signal == "BUY":
                for l in levels:
                    if abs(price - l) / price < 0.001:
                        logger.info(f"⛔ Resistenza vicina a {l:.5f}, BUY bloccato")
                        final_signal = "HOLD"
                        break
            elif final_signal == "SELL":
                for l in levels:
                    if abs(price - l) / price < 0.001:
                        logger.info(f"⛔ Supporto vicino a {l:.5f}, SELL bloccato")
                        final_signal = "HOLD"
                        break

            atr = (df["High"].max() - df["Low"].min()) / 10
            sl = price - 1.2 * atr if final_signal == "BUY" else price + 1.2 * atr
            tp = price + 1.2 * abs(price - sl) if final_signal == "BUY" else price - 1.2 * abs(price - sl)
            return final_signal, price, sl, tp, levels, sentiment_news, sentiment_x, session, trend_h1, trend_h4

        except Exception as e:
            logger.error(f"Errore: {e}")
            return "HOLD", 1.0, 0, 0, [], "", "", "", "", ""

    def execute(self):
        self.bridge.connect()
        positions = self.bridge.get_positions()
        signal, price, sl, tp, levels, sn, sx, sess, th1, th4 = self.get_ai_signal()
        logger.info(f"Segnale: {signal} @ {price:.5f} SL {sl:.5f} TP {tp:.5f}")
        logger.info(f"📰 News: {sn[:100]}")
        logger.info(f"🐦 X: {sx[:100]}")
        logger.info(f"⏰ Sessione: {sess}")
        logger.info(f"📈 Trend H1: {th1}, H4: {th4}")
        if levels:
            logger.info(f"📊 SR: {', '.join([f'{l:.5f}' for l in levels])}")

        if not self.risk.check(signal, price, sl):
            logger.info("⛔ Rischio negato")
            self.bridge.disconnect()
            return

        if not self.pm.validate(signal, price, sl, tp, positions):
            logger.info("⛔ Portfolio Manager ha bloccato")
            self.bridge.disconnect()
            return

        if signal == "BUY" and not positions:
            self.bridge.place_order('buy', 0.01, price, sl, tp)
            logger.info("✅ Eseguito BUY")
        elif signal == "SELL" and not positions:
            self.bridge.place_order('sell', 0.01, price, sl, tp)
            logger.info("✅ Eseguito SELL")
        else:
            logger.info("⏸️ HOLD")
        self.bridge.disconnect()

if __name__ == '__main__':
    orch = TradingOrchestrator()
    orch.execute()
