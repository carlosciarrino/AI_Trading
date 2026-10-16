from core.cognitive_orchestrator import CognitiveOrchestrator


class FakeRuntimeController:

    def get_runtime_state(self):
        return {
            "safe_mode": True
        }


class FakeRiskGovernor:

    trading_blocked = True


orchestrator = CognitiveOrchestrator(
    runtime_controller=FakeRuntimeController(),
    risk_governor=FakeRiskGovernor()
)


result = orchestrator.request_action(
    module="StrategyManager",
    action="EXECUTE_TRADE",
    priority=5,
    reason="test live trade"
)

print("\nRESULT:\n")
print(result)
