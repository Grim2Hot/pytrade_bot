import asyncio
from aiopubsub import Hub, Publisher, Subscriber, Key
import aiohttp


class Trader:
    def __init__(self, broker_api, hub: Hub):
        self.broker_api = broker_api
        self.hub = hub
        
        #self.publisher = Publisher(hub, prefix=Key('trading'))
        #self.subscriber = Subscriber(hub, prefix=Key('trading'))
        #self.subscriber.add_async_listener(Key('civ_update'), self.on_civ_update)
        