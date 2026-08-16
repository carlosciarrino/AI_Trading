# AI_BRIDGE - System Gateway

from core.cognitive_orchestrator import CognitiveOrchestrator


class SystemGateway:
    """
    Gateway centrale AI_BRIDGE.

    Responsabilità:
    - accesso unificato orchestrator
    - routing richieste
    - governance centralizzata
    """

    def __init__(
        self,
        runtime_controller=None,
        risk_governor=None,
        event_journal=None
    ):

        self.orchestrator = CognitiveOrchestrator(
            runtime_controller=runtime_controller,
            risk_governor=risk_governor,
            event_journal=event_journal
        )

    # ==========================================
    # ACTION REQUEST API
    # ==========================================

    def request_action(
        self,
        module,
        action,
        priority=1,
        reason="",
        metadata=None
    ):

        return self.orchestrator.request_action(
            module=module,
            action=action,
            priority=priority,
            reason=reason,
            metadata=metadata
        )
