from core.runtime_controller import (
    RuntimeController
)

runtime = RuntimeController()

runtime.set_system_status("RUNNING")

runtime.enable_safe_mode()

runtime.start_evolution_mode()

runtime.get_runtime_summary()
