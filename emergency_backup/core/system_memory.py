# AI_BRIDGE - System Memory Layer

from datetime import datetime


class SystemMemory:
    """
    Memoria centrale del sistema AI_BRIDGE.

    Funzioni:
    - memorizza errori
    - memorizza decisioni
    - recupera pattern ricorrenti
    """

    def __init__(self, event_journal=None):

        self.event_journal = event_journal

        self.error_memory = []
        self.decision_memory = []

    # =========================================
    # STORE ERROR
    # =========================================

    def store_error(self, error, context=None):

        record = {
            "type": "ERROR",
            "error": error,
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat()
        }

        self.error_memory.append(record)

        self._log("ERROR_STORED", record)

    # =========================================
    # STORE DECISION
    # =========================================

    def store_decision(self, decision):

        record = {
            "type": "DECISION",
            "decision": decision,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.decision_memory.append(record)

        self._log("DECISION_STORED", record)

    # =========================================
    # GET PATTERN ERRORS
    # =========================================

    def get_error_pattern(self, error_reason):

        matches = []

        for record in self.error_memory:

            if record["error"].get("reason") == error_reason:
                matches.append(record)

        return {
            "count": len(matches),
            "matches": matches
        }

    # =========================================
    # CHECK REPEATED ERROR
    # =========================================

    def is_repeated_error(self, error_reason, threshold=3):

        pattern = self.get_error_pattern(error_reason)

        return pattern["count"] >= threshold

    # =========================================
    # LOGGING
    # =========================================

    def _log(self, event_type, data):

        print(f"[MEMORY] {event_type}")

        if self.event_journal and hasattr(self.event_journal, "log_event"):
            self.event_journal.log_event({
                "type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            })
