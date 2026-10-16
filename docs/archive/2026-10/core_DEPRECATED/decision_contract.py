# AI_BRIDGE - Decision Contract Layer

from datetime import datetime


class DecisionContractValidator:
    """
    Controlla che ogni richiesta al sistema rispetti uno schema valido
    prima di entrare nell'orchestratore.
    """

    REQUIRED_FIELDS = {
        "module": str,
        "action": str,
        "priority": int
    }

    OPTIONAL_FIELDS = {
        "reason": str,
        "metadata": dict
    }

    def validate(self, request):

        errors = []

        # =========================
        # CHECK REQUIRED FIELDS
        # =========================

        for field, expected_type in self.REQUIRED_FIELDS.items():

            if field not in request:
                errors.append(f"MISSING_{field}")
                continue

            if not isinstance(request[field], expected_type):
                errors.append(f"INVALID_TYPE_{field}")

        # =========================
        # CHECK OPTIONAL FIELDS
        # =========================

        for field, expected_type in self.OPTIONAL_FIELDS.items():

            if field in request and not isinstance(request[field], expected_type):
                errors.append(f"INVALID_TYPE_{field}")

        # =========================
        # RESULT
        # =========================

        if errors:
            return {
                "allowed": False,
                "reason": "CONTRACT_VIOLATION",
                "errors": errors,
                "timestamp": datetime.utcnow().isoformat()
            }

        return {
            "allowed": True,
            "reason": "CONTRACT_OK",
            "timestamp": datetime.utcnow().isoformat()
        }

    def normalize(self, request):

        normalized = dict(request)

        # aggiunge metadata se manca
        if "metadata" not in normalized:
            normalized["metadata"] = {}

        # aggiunge reason se manca
        if "reason" not in normalized:
            normalized["reason"] = "UNSPECIFIED"

        return normalized
