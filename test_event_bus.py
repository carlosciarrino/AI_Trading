from core.event_bus import EventBus


bus = EventBus()


def on_trade_event(data):

    print("\n[TRADE EVENT RECEIVED]\n")

    print(data)


def on_risk_event(data):

    print("\n[RISK EVENT RECEIVED]\n")

    print(data)


bus.subscribe(

    "trade_opened",
    on_trade_event

)

bus.subscribe(

    "risk_alert",
    on_risk_event

)

bus.publish(

    "trade_opened",

    {

        "symbol": "EURUSD",

        "lot": 0.10,

        "confidence": 0.74

    }

)

bus.publish(

    "risk_alert",

    {

        "drawdown": 12,

        "message": "High risk detected"

    }

)
