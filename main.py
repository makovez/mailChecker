from EmailChecker.api.Api import Api
import asyncio


api = Api("combos/combo.txt")

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(api.start())
loop.run_until_complete(future)