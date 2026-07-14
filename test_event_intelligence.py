from core.event_bus import EventBus

from core.event_intelligence import (
    EventIntelligence
)


bus = EventBus()


# GENERA EVENTI TEST

for i in range(12):

    bus.publish(

        "trade_opened",

        {

            "trade_id": i

        }

    )


bus.publish(

    "risk_alert",

    {

        "drawdown": 16

    }

)

bus.publish(

    "failure_detected",

    {

        "module": "sync_engine"

    }

)


# ANALISI

engine = EventIntelligence()

engine.analyze_events()
