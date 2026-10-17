import time, os

# P031-bis: experience_agent ora e' solo un logger.
# La memoria vera e' in trading_memory.md, gestita da reflection_agent.py.
# Questo agente non scrive piu' in experiences.json.

EXPERIENCE_PATH = os.path.expanduser("~/AI_Trading/experiences.json")

def main():
    print("[experience] Agente avviato. Memoria in trading_memory.md (gestita da reflection_agent).", flush=True)
    while True:
        time.sleep(3600)

if __name__ == "__main__":
    main()
