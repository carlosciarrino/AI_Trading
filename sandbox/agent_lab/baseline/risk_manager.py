import datetime

# ----------------------------
# PARAMETRI PRINCIPALI
# ----------------------------

MAX_DAILY_LOSS_PERCENT = 3.0      # blocco se perdi 3% al giorno
MAX_DRAWDOWN_PERCENT = 10.0       # blocco totale sistema
RISK_PER_TRADE_PERCENT = 0.5      # rischio per singolo trade
MAX_TRADES_PER_DAY = 10

START_BALANCE = 10000  # cambia con il tuo conto reale

# ----------------------------
# STATO GIORNALIERO
# ----------------------------

state = {
    "day": None,
    "daily_loss": 0.0,
    "trades": 0,
    "equity_peak": START_BALANCE
}


# ----------------------------
# RESET GIORNALIERO
# ----------------------------

def reset_if_new_day():
    today = datetime.datetime.utcnow().date()

    if state["day"] != today:
        state["day"] = today
        state["daily_loss"] = 0.0
        state["trades"] = 0


# ----------------------------
# AGGIORNA EQUITY PEAK
# ----------------------------

def update_equity(current_equity):
    if current_equity > state["equity_peak"]:
        state["equity_peak"] = current_equity


# ----------------------------
# DRAW DOWN CHECK
# ----------------------------

def check_drawdown(current_equity):
    peak = state["equity_peak"]

    if peak <= 0:
        return True

    dd = ((peak - current_equity) / peak) * 100

    if dd >= MAX_DRAWDOWN_PERCENT:
        print("⛔ BLOCCO: DRAWDOWN MASSIMO RAGGIUNTO")
        return False

    return True


# ----------------------------
# DAILY LOSS CHECK
# ----------------------------

def check_daily_loss(current_equity):
    loss_percent = (state["daily_loss"] / START_BALANCE) * 100

    if loss_percent >= MAX_DAILY_LOSS_PERCENT:
        print("⛔ BLOCCO: PERDITA GIORNALIERA MASSIMA")
        return False

    return True


# ----------------------------
# LIMITI TRADING
# ----------------------------

def check_trade_limit():
    if state["trades"] >= MAX_TRADES_PER_DAY:
        print("⛔ BLOCCO: MAX TRADES RAGGIUNTO")
        return False

    return True


# ----------------------------
# CALCOLO LOTTO DINAMICO
# ----------------------------

def calculate_lot(balance):
    risk_amount = balance * (RISK_PER_TRADE_PERCENT / 100)

    # semplificato (poi lo rendiamo pro con pip value)
    lot = risk_amount / 1000

    if lot < 0.01:
        lot = 0.01

    if lot > 1.0:
        lot = 1.0

    return round(lot, 2)


# ----------------------------
# FUNZIONE PRINCIPALE
# ----------------------------

def risk_manager(current_equity):
    reset_if_new_day()

    update_equity(current_equity)

    if not check_drawdown(current_equity):
        return False, 0.0

    if not check_daily_loss(current_equity):
        return False, 0.0

    if not check_trade_limit():
        return False, 0.0

    lot = calculate_lot(current_equity)

    return True, lot


# ----------------------------
# REGISTRA TRADE (DA MT4)
# ----------------------------

def register_trade(result_profit):
    """
    MT4 deve chiamare questa funzione:
    profit > 0 = guadagno
    profit < 0 = perdita
    """

    state["trades"] += 1

    if result_profit < 0:
        state["daily_loss"] += abs(result_profit)
