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

    async def update_data(self, symbol: str, session: aiohttp.ClientSession = None):
        """
        Fetch data for a given symbol, convert the result into a Pandas DataFrame,
        and publish it as an update to the pub/sub system.
        """
        url = f"{self.broker_api}/{symbol}/data"
        # Allow session reuse if provided.
        close_session = False
        if session is None:
            session = aiohttp.ClientSession()
            close_session = True
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    try:
                        # Stuff
                        pass
                    except Exception as e:
                        print(f"Error processing data for {symbol}: {e}")
                        return
                    # Publish the new data for the symbol; subscribers on the specific key receive the DataFrame.
                    update_key = Key('data_update', symbol)
                    await self.publisher.publish(update_key, df)
                    print(f"Published updated data for {symbol}")
                else:
                    print(f"Failed to fetch data for {symbol} (HTTP {response.status})")
        except Exception as e:
            print(f"Exception fetching data for {symbol}: {e}")
        finally:
            if close_session:
                await session.close()

    async def update_all(self, symbols: list):
        """
        Given a list of symbols (e.g., 50 symbols), concurrently send API requests to get
        the latest data, and publish update events when each response is processed.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self.update_data(symbol, session) for symbol in symbols]
            await asyncio.gather(*tasks)

    def evaluate_civ(self, civ_data):
        # Evaluate the CIV data and decide whether to place an order
        if civ_data.get('BUY', 0) > self.risk_threshold:
            return {"symbol": "AAPL", "action": "BUY", "amount": 10}
        elif civ_data.get('SELL', 0) > self.risk_threshold:
            return {"symbol": "AAPL", "action": "SELL", "amount": 10}
        return None