from core.event_bus import EventBus


bus = EventBus()


def trade_handler(data):

    print("\n[TRADE HANDLER]\n")

    print(data)


bus.subscribe(

    "trade_opened",
    trade_handler

)

bus.publish(

    "trade_opened",

    {

        "symbol": "EURUSD",

        "lot": 0.20,

        "confidence": 0.81

    }

)

bus.publish(

    "risk_alert",

    {

        "drawdown": 14

    }

)

print("\nTEST COMPLETED\n")

