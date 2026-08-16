# AI_BRIDGE - Order Tracker

class OrderTracker:

    def __init__(self):

        self.active_orders = {}

    def register(self, ticket, strategy):

        self.active_orders[ticket] = {
            "strategy": strategy,
            "status": "OPEN"
        }

    def close(self, ticket, profit):

        if ticket in self.active_orders:

            self.active_orders[ticket]["status"] = "CLOSED"
            self.active_orders[ticket]["profit"] = profit

    def get_exposure(self):

        return len([
            o for o in self.active_orders.values()
            if o["status"] == "OPEN"
        ])
