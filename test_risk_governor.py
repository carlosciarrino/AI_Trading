from core.risk_governor import (
    RiskGovernor
)

governor = RiskGovernor()

result = governor.can_trade(

    confidence=0.72,
    drawdown=5

)

print("\nTRADE RESULT:\n")

print(result)
