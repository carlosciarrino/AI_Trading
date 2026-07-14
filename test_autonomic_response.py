from core.autonomic_response import (
    AutonomicResponseEngine
)

from core.runtime_controller import (
    RuntimeController
)


# RESET RUNTIME

runtime = RuntimeController()

runtime.disable_safe_mode()

runtime.stop_evolution_mode()

runtime.stop_recovery_mode()

runtime.set_system_status("RUNNING")


# TEST ENGINE

engine = AutonomicResponseEngine()


# TEST RISK ALERT

engine.process_anomaly(

    "risk_alert",

    {

        "drawdown": 18

    }

)


# MOSTRA STATO

runtime.get_runtime_summary()
