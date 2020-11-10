import asyncio
from proxybroker.providers import Provider
a = Provider("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all&simplified=true")



async def main():
    res = await a.get_proxies()
    print(res)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())