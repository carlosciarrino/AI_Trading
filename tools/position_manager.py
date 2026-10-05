import json, os, logging, time, yfinance as yf

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Configurazione
BREAK_EVEN_TRIGGER_PIPS = 15
BREAK_EVEN_OFFSET_PIPS = 2
TRAILING_STOP_PIPS = 20
TRAILING_STEP_PIPS = 5
PIP_VALUE = 0.0001
CHECK_INTERVAL = 60

ORDERS_FILE = os.path.expanduser("~/mt4_shared/orders.json")
SL_COMMANDS_FILE = os.path.expanduser("~/mt4_shared/sl_commands.json")

def get_orders():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE) as f:
        try:
            return json.load(f)
        except:
            return []

def write_sl_command(ticket, new_sl):
    """Scrive un comando di modifica SL in un file separato."""
    commands = []
    if os.path.exists(SL_COMMANDS_FILE):
        with open(SL_COMMANDS_FILE) as f:
            try:
                commands = json.load(f)
            except:
                commands = []
    # Evita duplicati
    commands = [c for c in commands if c.get("ticket") != ticket]
    commands.append({"ticket": ticket, "new_sl": round(new_sl, 5)})
    with open(SL_COMMANDS_FILE, "w") as f:
        json.dump(commands, f, indent=2)
    logger.info(f"  📝 Comando SL scritto per ticket {ticket}: {new_sl:.5f}")

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
    
    for order in orders:
        if order.get("status") != "open":
            continue
        
        entry = order.get("price", 0)
        current_sl = order.get("sl", 0)
        action = order.get("action", "buy")
        ticket = order.get("ticket", "N/A")
        break_even_done = order.get("break_even_applied", False)
        
        if entry == 0:
            continue
        
        if action == "buy":
            profit_pips = (current_price - entry) / PIP_VALUE
        else:
            profit_pips = (entry - current_price) / PIP_VALUE
        
        logger.info(f"  [{action}] ticket {ticket} | entry {entry:.5f} | prezzo {current_price:.5f} | profitto {profit_pips:.1f} pip")
        
        # FASE 1: Break-Even
        if profit_pips >= BREAK_EVEN_TRIGGER_PIPS and not break_even_done:
            if action == "buy":
                new_sl = entry + (BREAK_EVEN_OFFSET_PIPS * PIP_VALUE)
                if new_sl > current_sl:
                    write_sl_command(ticket, new_sl)
                    order["break_even_applied"] = True
                    logger.info(f"  ✅ Break-Even richiesto: SL {current_sl:.5f} → {new_sl:.5f}")
            else:
                new_sl = entry - (BREAK_EVEN_OFFSET_PIPS * PIP_VALUE)
                if new_sl < current_sl or current_sl == 0:
                    write_sl_command(ticket, new_sl)
                    order["break_even_applied"] = True
                    logger.info(f"  ✅ Break-Even richiesto: SL {current_sl:.5f} → {new_sl:.5f}")
    
    return True

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
