
from threading import Lock
import random, time, logging, asyncio
from Proxy import Proxy

class Proxies:

    def __init__(self, maxfails=3):
        self.proxies = []
        self.maxfails = maxfails
        self.lock = asyncio.Lock()

    async def add_proxy(self, proxy: Proxy):
        self.proxies.append(proxy)

    async def clear_fails(self, proxy: Proxy):
        async with self.lock:
            if proxy not in self.proxies:
                return await self.add_proxy(proxy) # Already removed but adding again as working
            ind = self.proxies.index(proxy)
            self.proxies[ind].fails = 0

    async def remove_proxy(self, proxy: Proxy):
        print("Removed: ", proxy.ip, proxy.port)
        self.proxies.remove(proxy)

    async def get_proxy(self):
        async with self.lock:
            while not self.proxies:
                await asyncio.sleep(1)
                #print(self.proxies)
                logging.debug("No proxy available. waiting...")
            
            return random.choice(self.proxies) 

    async def fail(self, proxy: Proxy):
        async with self.lock:
            print(proxy.ip, proxy)
            if proxy not in self.proxies: return False # Already removed
            ind = self.proxies.index(proxy)
            print(self.proxies[ind].ip, self.proxies[ind].fails)
            if self.proxies[ind].fails > self.maxfails:
                await self.remove_proxy(proxy) # max fails reached, remove proxy
            else:
                self.proxies[ind].fails += 1 # increase proxy fails
        

    