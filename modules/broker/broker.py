import asyncio
from aiopubsub import Hub, Publisher, Subscriber, Key
import aiohttp



class Broker:
    def __init__(self, broker_api, hub: Hub):
        self.broker_api = broker_api
        self.hub = hub
        self.publisher = Publisher(hub, prefix=Key('trading'))
        self.subscriber = Subscriber(hub, prefix=Key('trading'))
        self.subscriber.add_async_listener(Key('civ_update'), self.on_civ_update)

        # self.risk_threshold = 0.75 # Risk threshold for the broker
        # self.portfolio = {} # Portfolio dictionary to store asset positions

    async def on_civ_update(self, civ_data):
        # Temp idea function. civ_data represents Confidence Index Vector/Value.
        print("Received CIV data:", civ_data)
        order = self.evaluate_civ(civ_data)
        if order:
            await self.place_order(order)
            
    async def place_order(self, order):
        # Use aiohttp for non-blocking HTTP POST requests to commit the trade order.
        async with aiohttp.ClientSession() as session:
            async with session.post(self.broker_api_url, json=order) as response:
                if response.status == 200:
                    print("Order placed successfully:", order)
                else:
                    print("Failed to place order:", order)

    def evaluate_civ(self, civ_data):
        # Evaluate the CIV data and decide whether to place an order
        if civ_data.get('BUY', 0) > self.risk_threshold:
            return {"symbol": "AAPL", "action": "BUY", "amount": 10}
        elif civ_data.get('SELL', 0) > self.risk_threshold:
            return {"symbol": "AAPL", "action": "SELL", "amount": 10}
        return None

    async def run(self):
        # This run loop keeps the broker class alive.
        # In a production system, you might handle shutdown signals or integrate
        # the broker's run method into a larger main event loop.
        while True:
            await asyncio.sleep(1)

