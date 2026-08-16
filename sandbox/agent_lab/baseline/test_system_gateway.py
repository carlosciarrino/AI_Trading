from core.system_gateway import SystemGateway


class FakeRuntimeController:

    def get_runtime_state(self):

        return {
            "safe_mode": False
        }


class FakeRiskGovernor:

    trading_blocked = False


gateway = SystemGateway(
    runtime_controller=FakeRuntimeController(),
    risk_governor=FakeRiskGovernor()
)


result = gateway.request_action(
    module="StrategyManager",
    action="EXECUTE_TRADE",
    priority=5,
    reason="gateway integration test"
)


print("\nRESULT:\n")
print(result)
