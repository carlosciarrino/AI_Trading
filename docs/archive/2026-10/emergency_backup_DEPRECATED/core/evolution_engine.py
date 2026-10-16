import random
import copy

from core.strategy_manager import StrategyManager
from core.validation_engine import ValidationEngine
from core.rollback_engine import RollbackEngine
from core.performance_engine import PerformanceEngine


class EvolutionEngine:

    def __init__(self):

        self.strategy_manager = StrategyManager()

        self.validator = ValidationEngine()

        self.rollback = RollbackEngine()

        self.performance = PerformanceEngine()

    def mutate_strategy(self):

        current = self.strategy_manager.load_strategy()

        mutated = copy.deepcopy(current)

        mutation_type = random.choice([

            "ema_fast",
            "stop_loss",
            "take_profit",
            "confidence"

        ])

        if mutation_type == "ema_fast":

            mutated["ema_fast"] += random.randint(-2, 2)

        elif mutation_type == "stop_loss":

            mutated["stop_loss"] += random.randint(-3, 3)

        elif mutation_type == "take_profit":

            mutated["take_profit"] += random.randint(-5, 5)

        elif mutation_type == "confidence":

            mutated["confidence_threshold"] += random.uniform(-0.05, 0.05)

        print("\n[EVOLUTION] Mutation generated:\n")

        print(mutated)

        return mutated

    def evaluate_strategy(self, strategy):

        report = self.performance.analyze()

        if report is None:

            print("[EVOLUTION] No performance data.")

            return 0

        score = 0

        score += report["winrate"] * 0.4

        score += report["profit_factor"] * 30

        score += report["average_profit"] * 2

        final_score = score / 100

        print(f"\n[EVOLUTION SCORE] {final_score}\n")

        return final_score

    def evolve(self):

        current = self.strategy_manager.load_strategy()

        self.rollback.save_safe_strategy(current)

        candidate = self.mutate_strategy()

        valid, errors = self.validator.validate_strategy(candidate)

        if not valid:

            print("\n[VALIDATION FAILED]\n")

            for error in errors:

                print(f" - {error}")

            restored = self.rollback.restore_safe_strategy()

            if restored:

                self.strategy_manager.save_strategy(restored)

            return

        score = self.evaluate_strategy(candidate)

        if score > 0.60:

            print("[EVOLUTION] Candidate promoted.")

            self.strategy_manager.save_strategy(candidate)

        else:

            print("[EVOLUTION] Candidate rejected.")

            restored = self.rollback.restore_safe_strategy()

            if restored:

                self.strategy_manager.save_strategy(restored)
