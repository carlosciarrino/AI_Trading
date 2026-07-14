from core.runtime_controller import (
    RuntimeController
)

runtime = RuntimeController()

runtime.disable_safe_mode()

runtime.stop_evolution_mode()

runtime.stop_recovery_mode()

runtime.set_system_status("RUNNING")

runtime.get_runtime_summary()
