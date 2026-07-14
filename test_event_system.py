from core.event_engine import EventEngine


watch_path = "mt4_shared"

engine = EventEngine(watch_path)

engine.start()

engine.run_forever()
