# AI_BRIDGE - Meta Learning Engine

from datetime import datetime
import random
import copy


class MetaLearningEngine:
    """
    Sistema che evolve le strategie del Brain Pool.
    """

    def __init__(self, brain_pool, event_journal=None):

        self.brain_pool = brain_pool
        self.event_journal = event_journal

        # soglie evolutive
        self.prune_threshold = 0.85
        self.mutation_rate = 0.15

    # =========================================
    # MAIN LOOP
    # =========================================

    def evolve(self):

        scores = self.brain_pool.performance_score

        # 1. PRUNING
        self._prune_weak_brains(scores)

        # 2. MUTATION
        self._mutate_strong_brains(scores)

        self._log("META_LEARNING_CYCLE_COMPLETED", scores)

    # =========================================
    # PRUNING
    # =========================================

    def _prune_weak_brains(self, scores):

        for strategy, score in list(scores.items()):

            if score < self.prune_threshold:

                # degrada lentamente invece di eliminare brutale
                scores[strategy] *= 0.95

                self._log("BRAIN_DEGRADED", {
                    "strategy": strategy,
                    "score": scores[strategy]
                })

    # =========================================
    # MUTATION (CREAZIONE VARIANTI)
    # =========================================

    def _mutate_strong_brains(self, scores):

        for strategy, score in list(scores.items()):

            if score > 1.1:

                if random.random() < self.mutation_rate:

                    new_strategy = f"{strategy}_mut_{random.randint(1,999)}"

                    # copia comportamento base dal brain pool
                    self.brain_pool.performance_score[new_strategy] = score * 0.9

                    self._log("NEW_MUTATED_BRAIN", {
                        "parent": strategy,
                        "child": new_strategy
                    })

    # =========================================
    # LOGGING
    # =========================================

    def _log(self, event_type, data):

        print(f"[META_LEARNING] {event_type}")

        if self.event_journal and hasattr(self.event_journal, "log_event"):
            self.event_journal.log_event({
                "type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            })
