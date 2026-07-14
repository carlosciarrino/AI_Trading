# AI_BRIDGE - Optimization Engine

from datetime import datetime


class OptimizationEngine:
    """
    Ottimizza il comportamento del sistema AI_BRIDGE
    basandosi su pattern di errore e decisione.

    NON modifica codice.
    Modifica solo parametri interni (safe optimization).
    """

    def __init__(self, memory, event_journal=None):

        self.memory = memory
        self.event_journal = event_journal

        # parametri dinamici ottimizzabili
        self.parameters = {
            "permission_strictness": 1.0,
            "safe_mode_sensitivity": 1.0,
            "auto_heal_aggressiveness": 1.0
        }

    # =========================================
    # MAIN OPTIMIZATION ENTRY
    # =========================================

    def optimize(self):

        insights = {
            "adjustments": [],
            "timestamp": datetime.utcnow().isoformat()
        }

        # 1. analisi errori ripetuti
        repeated_contract = self.memory.is_repeated_error("CONTRACT_VIOLATION")
        repeated_permission = self.memory.is_repeated_error("PERMISSION_DENIED")

        # =====================================
        # OPTIMIZATION RULES
        # =====================================

        # CONTRACT VIOLATIONS FREQUENTI
        if repeated_contract:
            self.parameters["permission_strictness"] *= 1.1

            insights["adjustments"].append({
                "type": "INCREASE_STRICTNESS",
                "target": "permission_strictness"
            })

        # PERMISSION ERROR FREQUENTI
        if repeated_permission:
            self.parameters["auto_heal_aggressiveness"] *= 1.1

            insights["adjustments"].append({
                "type": "INCREASE_AUTO_HEAL",
                "target": "auto_heal_aggressiveness"
            })

        # SAFE MODE TROPPO ATTIVO
        if self._safe_mode_over_triggered():
            self.parameters["safe_mode_sensitivity"] *= 0.9

            insights["adjustments"].append({
                "type": "REDUCE_SAFE_MODE_SENSITIVITY"
            })

        self._log("OPTIMIZATION_RUN", insights)

        return {
            "status": "OPTIMIZED",
            "parameters": self.parameters,
            "insights": insights
        }

    # =========================================
    # SIMPLE HEURISTIC
    # =========================================

    def _safe_mode_over_triggered(self):

        total = len(self.memory.error_memory)

        if total < 5:
            return False

        safe_mode_blocks = 0

        for record in self.memory.error_memory:
            if record["error"].get("reason") == "SAFE_MODE_BLOCK":
                safe_mode_blocks += 1

        return safe_mode_blocks / total > 0.5

    # =========================================
    # LOGGING
    # =========================================

    def _log(self, event_type, data):

        print(f"[OPTIMIZATION] {event_type}")

        if self.event_journal and hasattr(self.event_journal, "log_event"):
            self.event_journal.log_event({
                "type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            })
