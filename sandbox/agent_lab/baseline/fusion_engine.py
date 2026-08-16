from risk_manager import risk_manager
from decision import make_decision

# ----------------------------
# CONFIGURAZIONE BASE
# ----------------------------

BASE_BALANCE = 10000

MIN_LOT = 0.01
MAX_LOT = 1.0


# ----------------------------
# NORMALIZZAZIONE SCORE
# ----------------------------

def normalize_score(score):
    """
    Converte score in range 0 → 1
    """

    if score > 10:
        score = 10
    if score < -10:
        score = -10

    return abs(score) / 10


# ----------------------------
# CALCOLO LOTTO INTELLIGENTE
# ----------------------------

def calculate_lot(score, equity):

    strength = normalize_score(score)

    risk_ok, base_lot = risk_manager(equity)

    if not risk_ok:
        return 0.0

    # scaling intelligente
    lot = base_lot * (0.5 + strength)

    if lot < MIN_LOT:
        lot = MIN_LOT

    if lot > MAX_LOT:
        lot = MAX_LOT

    return round(lot, 2)


# ----------------------------
# FUSION ENGINE PRINCIPALE
# ----------------------------

def get_fusion_decision(equity):

    decision, risk = make_decision()

    # recupera score globale indirettamente
    # (versione semplice: ricaviamo rischio da decisione)

    score_map = {
        "BUY": 7,
        "SELL": -7,
        "NONE": 0
    }

    score = score_map.get(decision, 0)

    lot = calculate_lot(score, equity)

    # filtro finale sicurezza
    if lot == 0:
        return "NONE", "LOW", 0.0

    if abs(score) < 4:
        return "NONE", "LOW", 0.0

    return decision, risk, lot
