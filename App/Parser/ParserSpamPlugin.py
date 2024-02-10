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
        await update_followers_db(
            account_inst_dal=account_inst_dal
        )
        aioschedule.every().day.do(update_followers_db, account_inst_dal)
        while True:
            accounts = await account_inst_dal.getSessionNamesWithTrueStatus()
            tasks = []
            for account_name in accounts:
                account = await account_inst_dal.getAccountBySessionName(account_name)
                if account and account.target_channels:
                    
                    for follower in followers_db:
                        proxies_list = await proxy_dal.getProxyAddressById(
                            account_inst_id=account.id
                        )
                        if (follower["id"] == account.id):
                            instagramParser = InstagramParser(
                                login=account_name,
                                password="",
                                proxy=proxies_list[0]
                            )
                            proxies_list.append(proxies_list[0])
                            proxies_list.remove(proxies_list[0])
                            task = asyncio.create_task(
                                instagramParser.async_send_message(account.message, follower["username"])
                            )
                            tasks.append(task)
                    
                await asyncio.gather(*tasks)
                await asyncio.sleep(60)

async def update_followers_db(account_inst_dal: AccountInstDAL):
    global followers_db
    followers_db = await account_inst_dal.getAllFollowers()

if __name__ == "__main__":
    asyncio.run(mainLayer())

