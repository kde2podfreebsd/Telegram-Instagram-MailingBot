import asyncio
import random
import uvloop
from selenium.common.exceptions import TimeoutException

from App.Database.DAL.AccountInstDAL import AccountInstDAL
from App.Database.DAL.ProxyDAL import ProxyAddressDAL
from App.Database.session import async_session
from App.Parser.InstagramParser import InstagramParser, InstagramParserExceptions
import aioschedule

async def sleep():
    await asyncio.sleep(10)

async def mainLayer():
    async with async_session() as session:
        account_inst_dal = AccountInstDAL(session)
        proxy_dal = ProxyAddressDAL(session)
        uvloop.install()

        while True:
            accounts = await account_inst_dal.getSessionNamesWithTrueStatus()

            for account_name in accounts:
                account = await account_inst_dal.getAccountBySessionName(account_name)
                if account and account.target_channels:
                    followers = await account_inst_dal.getFollowers(account_inst_id=account.id)
                    for follower in followers:
                        proxies_list = await proxy_dal.getProxyAddressById(
                            account_inst_id=account.id
                        )
                        instagramParser = InstagramParser(
                            login=account_name,
                            password="",
                            proxy=proxies_list[0]
                        )
                        proxies_list.append(proxies_list[0])
                        proxies_list.remove(proxies_list[0])
                        await instagramParser.async_send_message(account.message, follower)
                        await asyncio.sleep(5)
                await asyncio.sleep(60*account.delay)

if __name__ == "__main__":
    asyncio.run(mainLayer())
