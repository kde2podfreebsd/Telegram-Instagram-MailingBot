import asyncio
import uvloop

from App.Database.DAL.AccountInstDAL import AccountInstDAL
from App.Database.DAL.ProxyDAL import ProxyAddressDAL
from App.Database.session import async_session
from App.Parser.InstagramParser import InstagramParser
import aioschedule

async def mainLayer():
    async with async_session() as session:
        account_inst_dal = AccountInstDAL(session)
        proxy_dal = ProxyAddressDAL(session)
        uvloop.install()
        await update_followers_db(
            account_inst_dal=account_inst_dal
        )
        aioschedule.every().day.do(update_followers_db, account_inst_dal)
      
        accounts = await account_inst_dal.getSessionNamesWithTrueStatus()
        for account_name in accounts:
            account = await account_inst_dal.getAccountBySessionName(account_name)
            if account and account.target_channels:
                await parser_thread(
                    account_name=account_name,
                    message=account.message,
                    id=account.id,
                    proxy_dal=proxy_dal
                ) 
                aioschedule.every(account.delay).minutes.do(parser_thread, account_name, account.message, account.id, proxy_dal)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(5)

async def parser_thread(
        account_name: str, 
        message: str, 
        id: int, 
        proxy_dal: ProxyAddressDAL
    ):
    tasks = []
    for follower in followers_db:
        proxies_list = await proxy_dal.getProxyAddressById(
            account_inst_id=id
        )
        if (follower["id"] == id):
            instagramParser = InstagramParser(
                login=account_name,
                password="",
                proxy=proxies_list[0]
            )
            proxies_list.append(proxies_list[0])
            proxies_list.remove(proxies_list[0])
            task = asyncio.create_task(
                instagramParser.async_send_message(message, follower["username"])
            )
            tasks.append(task)
    await asyncio.gather(*tasks)
                            
async def update_followers_db(account_inst_dal: AccountInstDAL):
    global followers_db
    followers_db = await account_inst_dal.getAllFollowers()

if __name__ == "__main__":
    asyncio.run(mainLayer())

