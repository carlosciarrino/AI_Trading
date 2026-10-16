# AI_BRIDGE - Auto Healing Engine

from datetime import datetime


class AutoHealingEngine:
    """
    Sistema di auto-riparazione controllata.
    Non modifica codice, ma corregge input e stati.
    """

    def __init__(self, event_journal=None):
        self.event_journal = event_journal

    def attempt_heal(self, error, context=None):

        context = context or {}

        reason = error.get("reason", "UNKNOWN_ERROR")

        if reason == "CONTRACT_VIOLATION":
            return self._heal_contract_violation(error, context)

        if reason == "PERMISSION_DENIED":
            return self._heal_permission(error, context)

        if reason == "SAFE_MODE_BLOCK":
            return self._heal_safe_mode(error, context)

        return self._no_heal(error)

    # =========================================
    # CONTRACT HEAL
    # =========================================

    def _heal_contract_violation(self, error, context):

        request = context.get("request", {})

        fixed = dict(request)

        if "metadata" not in fixed:
            fixed["metadata"] = {}

        if "reason" not in fixed:
            fixed["reason"] = "AUTO_HEALED"

        self._log("CONTRACT_HEALED", fixed)

        return {
            "healed": True,
            "action": "RETRY_REQUEST",
            "request": fixed,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================================
    # PERMISSION HEAL
    # =========================================

    def _heal_permission(self, error, context):

        request = context.get("request", {})

        fallback = dict(request)
        fallback["reason"] = "PERMISSION_FALLBACK"

        self._log("PERMISSION_HEAL_ATTEMPT", fallback)

        return {
            "healed": False,
            "action": "ESCALATE_OR_REJECT",
            "request": fallback,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================================
    # SAFE MODE HEAL
    # =========================================

    def _heal_safe_mode(self, error, context):

        request = context.get("request", {})

        modified = dict(request)
        modified["action"] = "NO_OP"

        self._log("SAFE_MODE_ADJUSTED", modified)

        return {
            "healed": True,
            "action": "RETRY_WITH_ALTERNATIVE",
            "request": modified,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================================
    # FALLBACK
    # =========================================

    def _no_heal(self, error):

        self._log("NO_HEAL_AVAILABLE", error)

        return {
            "healed": False,
            "action": "FAIL",
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }

    # =========================================
    # LOGGING
    # =========================================

    def _log(self, event_type, data):

        print(f"[AUTO_HEALING] {event_type}")

        if self.event_journal and hasattr(self.event_journal, "log_event"):
            self.event_journal.log_event({
                "type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            })
