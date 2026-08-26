import sys, json, time, logging, os, requests
from datetime import datetime
from core.mt4_bridge import MT4Bridge
from tools.live_data import get_recent
from tools.risk_manager import RiskManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class TradingOrchestrator:
    def __init__(self):
        with open('mt4_bridge_config.json', 'r') as f:
            config = json.load(f)
        self.bridge = MT4Bridge(config=config)
        self.risk = RiskManager()
        logger.info("Orchestrator init OK")

    def get_ai_signal(self, symbol="EUR/USD"):
        try:
            df = get_recent(symbol, interval="15min", length=20)
            data_str = df.tail(10).to_string()
            prompt = f"""
Sei un analista di trading esperto. Usa solo dati price action e volume per prevedere il movimento a breve termine (prossime 1-2 ore). Riconosci pattern di supporto/resistenza, breakout, e momentum. Non usare indicatori lagging. Dai un segnale BUY/SELL/HOLD con breve giustificazione basata solo sui dati forniti.

Dati:
{data_str}

Decisione (BUY/SELL/HOLD):
"""
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.2:3b", "prompt": prompt, "stream": False},
                timeout=30
            )
            if resp.status_code != 200:
                logger.error("Ollama non risponde")
                return "HOLD", 1.0, 0, 0
            result = resp.json().get("response", "")
            logger.info(f"AI: {result}")
            signal = "HOLD"
            for word in ["BUY", "SELL", "HOLD"]:
                if word in result.upper():
                    signal = word
                    break
            price = df["Close"].iloc[-1]
            atr = (df["High"].max() - df["Low"].min()) / 10
            sl = price - 1.2 * atr if signal == "BUY" else price + 1.2 * atr
            tp = price + 1.2 * abs(price - sl) if signal == "BUY" else price - 1.2 * abs(price - sl)
            return signal, price, sl, tp
        except Exception as e:
            logger.error(f"Errore: {e}")
            return "HOLD", 1.0, 0, 0

    def execute(self):
        self.bridge.connect()
        positions = self.bridge.get_positions()
        signal, price, sl, tp = self.get_ai_signal()
        logger.info(f"Segnale: {signal} @ {price:.5f} SL {sl:.5f} TP {tp:.5f}")
        if not self.risk.check(signal, price, sl):
            logger.info("⛔ Rischio negato")
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
