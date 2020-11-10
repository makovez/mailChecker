import asyncio, aiohttp, time
from proxybroker import Broker
from Proxies import Proxies, Proxy
from concurrent.futures._base import TimeoutError

proxis = Proxies()
COUNT = 0
PROVIDERS = ['https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all&simplified=true']
async def check(session, host, port, timeout=6):
    try:
        async with session.get('https://api.ipify.org?format=json', proxy=f"http://{host}:{port}", timeout=timeout) as response:
            html = await response.json()
            if html and html["ip"]:
                print(f"[!] {host}:{port}")
                await proxis.add_proxy(Proxy(host, port))
                return True
            print(f"[x] {host}:{port}, {html}")
            return False
    except Exception as e:
        print(f"[x] {host}:{port}, {e}")
        return False

async def show(proxies):
	tasks = []

	conn = aiohttp.TCPConnector(ssl=False, limit=None)
	async with aiohttp.ClientSession(connector=conn) as session:
		while True:
			proxy = await proxies.get()
			if proxy is None: break
			task = asyncio.ensure_future(check(session, proxy.host, proxy.port))
			tasks.append(task)

		await asyncio.gather(*tasks)


async def fetch_url(session, timeout=8):
    global COUNT
    
    while len(proxis.proxies) < 10:
        print(proxis.proxies)
        time.sleep(1)
        print("Not ready!")

    proxy = await proxis.get_proxy()
    try:
        async with session.get('https://app.sharethemeal.org', proxy=f"http://{proxy.ip}:{proxy.port}", timeout=timeout) as response:
            res = await response.read()
            if res == b"OK":
                COUNT += 1
                print("Ok", COUNT, proxy.ip, proxy.port)    
                await proxis.clear_fails(proxy)  
                return True
            print("Fail")
            return await proxis.fail(proxy)
    except aiohttp.ClientError:
        print("Client Exception")
        return await proxis.fail(proxy)
    except TimeoutError:
        print("Timeout Exception")
        return await proxis.fail(proxy)
        

        
async def fetch():
    tasks = []

    conn = aiohttp.TCPConnector(ssl=False, limit=None)
    async with aiohttp.ClientSession(connector=conn) as session:
        for _ in range(1500):
            task = asyncio.ensure_future(fetch_url(session))
            await asyncio.sleep(0.01)
            tasks.append(task)

        await asyncio.gather(*tasks)
        print("end")


proxies = asyncio.Queue()
broker = Broker(proxies)
tasks = asyncio.gather(
    broker.find(types=['HTTPS', 'HTTP'], verify_ssl=False),
    show(proxies))


loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)
