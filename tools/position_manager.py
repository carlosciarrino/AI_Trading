import json, os, logging, time, yfinance as yf

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Configurazione
BREAK_EVEN_TRIGGER_PIPS = 15
BREAK_EVEN_OFFSET_PIPS = 2
TRAILING_STOP_PIPS = 20
TRAILING_STEP_PIPS = 5
PIP_VALUE = 0.0001  # EUR/USD
CHECK_INTERVAL = 60  # secondi

def get_orders():
    orders_file = os.path.expanduser("~/mt4_shared/orders.json")
    if not os.path.exists(orders_file):
        return []
    with open(orders_file) as f:
        try:
            return json.load(f)
        except:
            return []

def save_orders(orders):
    orders_file = os.path.expanduser("~/mt4_shared/orders.json")
    with open(orders_file, "w") as f:
        json.dump(orders, f, indent=2)

def get_current_price(symbol="EURUSD=X"):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            return None
        return float(data["Close"].iloc[-1])
    except Exception as e:
        logger.error(f"Errore prezzo {symbol}: {e}")
        return None

def check_and_update_positions():
    orders = get_orders()
    if not orders:
        return False
    
    current_price = get_current_price("EURUSD=X")
    if current_price is None:
        logger.warning("Prezzo non disponibile, salto il controllo.")
        return False
    
    logger.info(f"Prezzo corrente EURUSD: {current_price:.5f}")
    updated = False
    
    for order in orders:
        if order.get("status") != "open":
            continue
        
        entry = order.get("price", 0)
        current_sl = order.get("sl", 0)
        action = order.get("action", "buy")
        ticket = order.get("ticket", "N/A")
        
        if entry == 0:
            continue
        
        # Calcola profitto in pip
        if action == "buy":
            profit_pips = (current_price - entry) / PIP_VALUE
        else:
            profit_pips = (entry - current_price) / PIP_VALUE
        
        logger.info(f"  [{action}] ticket {ticket} | entry {entry:.5f} | prezzo {current_price:.5f} | profitto {profit_pips:.1f} pip")
        
        # FASE 1: Break-Even
        if profit_pips >= BREAK_EVEN_TRIGGER_PIPS and not order.get("break_even_applied"):
            if action == "buy":
                new_sl = entry + (BREAK_EVEN_OFFSET_PIPS * PIP_VALUE)
                if new_sl > current_sl:
                    order["new_sl"] = round(new_sl, 5)
                    order["break_even_applied"] = True
                    updated = True
                    logger.info(f"  ✅ Break-Even richiesto: SL {current_sl:.5f} → {new_sl:.5f}")
            else:
                new_sl = entry - (BREAK_EVEN_OFFSET_PIPS * PIP_VALUE)
                if new_sl < current_sl or current_sl == 0:
                    order["new_sl"] = round(new_sl, 5)
                    order["break_even_applied"] = True
                    updated = True
                    logger.info(f"  ✅ Break-Even richiesto: SL {current_sl:.5f} → {new_sl:.5f}")
        
        # FASE 2: Trailing Stop (solo dopo break-even)
        if order.get("break_even_applied") and profit_pips > BREAK_EVEN_TRIGGER_PIPS + TRAILING_STOP_PIPS:
            if action == "buy":
                trailing_sl = current_price - (TRAILING_STOP_PIPS * PIP_VALUE)
                last_sl = order.get("new_sl", order.get("sl", 0))
                if trailing_sl > last_sl + (TRAILING_STEP_PIPS * PIP_VALUE):
                    order["new_sl"] = round(trailing_sl, 5)
                    updated = True
                    logger.info(f"  📈 Trailing richiesto: SL {last_sl:.5f} → {trailing_sl:.5f}")
            else:
                trailing_sl = current_price + (TRAILING_STOP_PIPS * PIP_VALUE)
                last_sl = order.get("new_sl", order.get("sl", 999))
                if trailing_sl < last_sl - (TRAILING_STEP_PIPS * PIP_VALUE):
                    order["new_sl"] = round(trailing_sl, 5)
                    updated = True
                    logger.info(f"  📉 Trailing richiesto: SL {last_sl:.5f} → {trailing_sl:.5f}")
    
    if updated:
        save_orders(orders)
        logger.info("✅ Modifiche SL richieste. L'EA le applicherà al prossimo tick.")
    return updated

def main():
    logger.info("Position Manager avviato. Controllo ogni 60 secondi...")
    while True:
        try:
            check_and_update_positions()
        except Exception as e:
            logger.error(f"Errore: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
