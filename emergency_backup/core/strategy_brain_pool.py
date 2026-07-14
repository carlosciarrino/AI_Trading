# AI_BRIDGE - Strategy Brain Pool

from datetime import datetime
import random


class StrategyBrainPool:
    """
    Simula più "cervelli strategici" indipendenti.

    Ogni cervello propone una decisione diversa.
    Il sistema poi seleziona la migliore.
    """

    def __init__(self, memory, event_journal=None):

        self.memory = memory
        self.event_journal = event_journal

        self.brains = [
            self.risk_averse_brain,
            self.aggressive_brain,
            self.balanced_brain
        ]

        self.performance_score = {
            "risk_averse": 1.0,
            "aggressive": 1.0,
            "balanced": 1.0
        }

    # =========================================
    # MAIN ENTRY
    # =========================================

    def generate_decisions(self, request):

        candidates = []

        for brain in self.brains:

            decision = brain(request)

            candidates.append(decision)

        self._log("CANDIDATES_GENERATED", candidates)

        return candidates

    # =========================================
    # BRAINS
    # =========================================

    def risk_averse_brain(self, request):

        return {
            "strategy": "risk_averse",
            "action": request["action"] if random.random() > 0.7 else "NO_OP",
            "confidence": 0.9,
            "risk": 0.2
        }

    def aggressive_brain(self, request):

        return {
            "strategy": "aggressive",
            "action": request["action"],
            "confidence": 0.7,
            "risk": 0.8
        }

    def balanced_brain(self, request):

        return {
            "strategy": "balanced",
            "action": request["action"],
            "confidence": 0.8,
            "risk": 0.5
        }

    # =========================================
    # SELECTION ENGINE
    # =========================================

    def select_best(self, candidates):

        scored = []

        for c in candidates:

            score = self._score(c)

            scored.append((score, c))

        scored.sort(reverse=True, key=lambda x: x[0])

        best = scored[0][1]

        self._log("BEST_STRATEGY_SELECTED", best)

        return best

    # =========================================
    # SCORING FUNCTION
    # =========================================

    def _score(self, candidate):

        strategy = candidate["strategy"]

        base = self.performance_score.get(strategy, 1.0)

        confidence = candidate.get("confidence", 0.5)
        risk = candidate.get("risk", 0.5)

        # formula semplice ma efficace
        return (base * confidence) - (risk * 0.5)

    # =========================================
    # FEEDBACK LOOP
    # =========================================

    def update_performance(self, strategy, success=True):

        if success:
            self.performance_score[strategy] *= 1.05
        else:
            self.performance_score[strategy] *= 0.95

        self._log("STRATEGY_UPDATED", {
            "strategy": strategy,
            "score": self.performance_score[strategy]
        })

    # =========================================
    # LOGGING
    # =========================================

    def _log(self, event_type, data):

        print(f"[STRATEGY_POOL] {event_type}")

        if self.event_journal and hasattr(self.event_journal, "log_event"):
            self.event_journal.log_event({
                "type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            })
