import json, os, time, random, subprocess, logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class AutoReflect:
    def __init__(self):
        self.orders_file = Path(os.path.expanduser('~/mt4_shared/orders.json'))
        self.prompt_file = Path('prompts.py')
        self.best_prompt = None
        self.best_score = -float('inf')
        self.history_file = 'reflect_history.json'
        self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file) as f:
                self.history = json.load(f)
        else:
            self.history = {'attempts': [], 'best_score': -float('inf'), 'best_prompt': ''}
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)

    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def get_trades(self):
        if not self.orders_file.exists():
            return []
        with open(self.orders_file) as f:
            try:
                orders = json.load(f)
                return [o for o in orders if 'pnl' in o]
            except:
                return []

    def evaluate_prompt(self, prompt_variant):
        # Simula backtest con il nuovo prompt
        # Da implementare: chiamare orchestrator con prompt modificato e calcolare profit factor
        score = random.uniform(-10, 20)  # placeholder
        return score

    def mutate_prompt(self):
        # Legge il prompt corrente e applica una modifica casuale
        with open(self.prompt_file) as f:
            content = f.read()
        # Aggiunge o modifica una regola
        rules = [
            "Usa il volume come conferma.",
            "Cerca divergenze tra prezzo e RSI.",
            "Considera i livelli di Fibonacci.",
            "Priorità ai breakout.",
            "Aggiungi filtro trend con SMA 200.",
            "Usa solo le prime 3 candele del pattern.",
            "Applica trailing stop dinamico."
        ]
        new_rule = random.choice(rules)
        if new_rule not in content:
            content = content.replace('Sei un trader', f'Sei un trader. Regola aggiuntiva: {new_rule}.')
        return content

    def run_cycle(self):
        logger.info("🔄 Ciclo di auto-riflessione avviato.")
        trades = self.get_trades()
        if len(trades) < 10:
            logger.info("⏸️ Troppi pochi trade per riflettere (<10).")
            return

        # 1. Genera variante del prompt
        new_prompt = self.mutate_prompt()
        # 2. Valuta la variante (backtest simulato)
        score = self.evaluate_prompt(new_prompt)
        # 3. Se migliora, salva
        if score > self.best_score:
            self.best_score = score
            self.best_prompt = new_prompt
            with open(self.prompt_file, 'w') as f:
                f.write(new_prompt)
            logger.info(f"✅ Nuovo prompt migliore: {score:.2f}")
        else:
            logger.info(f"❌ Prompt peggiore: {score:.2f} (best: {self.best_score:.2f})")

        # 4. Registra tentativo
        self.history['attempts'].append({
            'time': datetime.now().isoformat(),
            'score': score,
            'best_score': self.best_score
        })
        self.save_history()
        logger.info("✅ Ciclo completato.")

if __name__ == '__main__':
    reflect = AutoReflect()
    reflect.run_cycle()
