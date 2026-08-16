# AI_BRIDGE - Learning Loop Engine

from datetime import datetime


class LearningLoop:
    """
    Analizza la memoria del sistema e individua pattern ripetuti.

    Obiettivo:
    - capire quali errori si ripetono
    - identificare moduli problematici
    - suggerire miglioramenti strutturali
    """

    def __init__(self, memory, event_journal=None):

        self.memory = memory
        self.event_journal = event_journal

    # =========================================
    # MAIN ANALYSIS
    # =========================================

    def analyze(self):

        error_patterns = self._analyze_errors()
        decision_patterns = self._analyze_decisions()

        insights = {
            "error_patterns": error_patterns,
            "decision_patterns": decision_patterns,
            "timestamp": datetime.utcnow().isoformat()
        }

        self._log("LEARNING_ANALYSIS_COMPLETE", insights)

        return insights

    # =========================================
    # ERROR ANALYSIS
    # =========================================

    def _analyze_errors(self):

        grouped = {}

        for record in self.memory.error_memory:

            reason = record["error"].get("reason", "UNKNOWN")

            if reason not in grouped:
                grouped[reason] = {
                    "count": 0,
                    "modules": set()
                }

            grouped[reason]["count"] += 1

            module = record["context"].get("module")
            if module:
                grouped[reason]["modules"].add(module)

        # convert sets to lists (JSON safe)
        for k in grouped:
            grouped[k]["modules"] = list(grouped[k]["modules"])

        return grouped

    # =========================================
    # DECISION ANALYSIS
    # =========================================

    def _analyze_decisions(self):

        stats = {
            "approved": 0,
            "denied": 0,
            "reasons": {}
        }

        for record in self.memory.decision_memory:

            decision = record["decision"]

            if decision.get("allowed"):
                stats["approved"] += 1
            else:
                stats["denied"] += 1

            reason = decision.get("reason", "UNKNOWN")

            if reason not in stats["reasons"]:
                stats["reasons"][reason] = 0

            stats["reasons"][reason] += 1

        return stats

    # =========================================
    # INSIGHT HELPERS
    # =========================================

    def get_most_common_error(self, analysis):

        errors = analysis.get("error_patterns", {})

        if not errors:
            return None

        return max(errors.items(), key=lambda x: x[1]["count"])

    def get_problematic_modules(self, analysis):

        module_count = {}

        for reason, data in analysis.get("error_patterns", {}).items():

            for module in data.get("modules", []):

                if module not in module_count:
                    module_count[module] = 0

                module_count[module] += data["count"]

        return module_count

    # =========================================
    # LOGGING
    # =========================================

    def _log(self, event_type, data):

        print(f"[LEARNING_LOOP] {event_type}")

        if self.event_journal and hasattr(self.event_journal, "log_event"):
            self.event_journal.log_event({
                "type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            })
