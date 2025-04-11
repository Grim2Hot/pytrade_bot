from modules import *
from aiopubsub import Hub, Publisher, Subscriber, Key
import asyncio
import aiohttp



while True:
    try:
        # Create a Hub instance
        hub = Hub()
        
        # Initialize the Broker and Trader with the Hub instance
        broker_api = "http://example.com/api"  # Replace with actual API URL
        broker = Broker(broker_api, hub)
        trader = Trader(broker_api, hub)
        
        # Start the event loop to run the Broker and Trader
        asyncio.run(hub.run())
        
    except Exception as e:
        print(f"An error occurred: {e}")