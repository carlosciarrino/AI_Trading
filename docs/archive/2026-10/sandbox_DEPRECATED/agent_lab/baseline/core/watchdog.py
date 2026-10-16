# AI_BRIDGE - Watchdog System

import time


class Watchdog:
    """
    Sistema di sicurezza che monitora crash e blocchi.
    """

    def __init__(self, monitoring, persistence):

        self.monitoring = monitoring
        self.persistence = persistence

        self.last_heartbeat = time.time()
        self.max_silence = 10  # secondi

    # =========================================
    # HEARTBEAT UPDATE
    # =========================================

    def heartbeat(self):

        self.last_heartbeat = time.time()

    # =========================================
    # CHECK SYSTEM
    # =========================================

    def check(self):

        silence = time.time() - self.last_heartbeat

        if silence > self.max_silence:
            print("[WATCHDOG] SYSTEM SILENCE DETECTED → RECOVERY MODE")

            return {
                "action": "RECOVERY",
                "reason": "HEARTBEAT_TIMEOUT"
            }

        return {
            "action": "OK"
        }
