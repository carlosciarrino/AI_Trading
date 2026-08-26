import os, json, time, logging, subprocess
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

ORDERS_FILE = os.path.expanduser("~/mt4_shared/orders.json")

def get_real_positions_from_mt4():
    """
    Da implementare: collegamento reale a MT4 (via file condiviso o API).
    Per ora, simula il recupero delle posizioni reali.
    """
    # TODO: Sostituire con lettura effettiva da MT4 (via Expert Advisor o file condiviso)
    # Per ora, torniamo lista vuota per non creare falsi ordini
    return []

def reconcile_orders():
    if not os.path.exists(ORDERS_FILE):
        logger.warning("File ordini non trovato.")
        return

    with open(ORDERS_FILE, 'r') as f:
        orders = json.load(f)

    real_positions = get_real_positions_from_mt4()
    real_order_ids = [p.get('order_id') for p in real_positions if p.get('order_id')]

    updated = False
    for order in orders:
        if order.get('status') == 'open' and order.get('order_id') not in real_order_ids:
            order['status'] = 'pending'
            updated = True
            logger.warning(f"Ordine {order.get('order_id')} non trovato su MT4. Stato: pending.")
        elif order.get('status') == 'pending' and order.get('order_id') in real_order_ids:
            order['status'] = 'open'
            updated = True
            logger.info(f"Ordine {order.get('order_id')} confermato su MT4.")

    if updated:
        with open(ORDERS_FILE, 'w') as f:
            json.dump(orders, f, indent=2)
        logger.info("File ordini aggiornato con stato reale.")

def main():
    logger.info("Reconciliation Agent avviato. Controllo ogni 60 secondi...")
    while True:
        reconcile_orders()
        time.sleep(60)

if __name__ == "__main__":
    main()
