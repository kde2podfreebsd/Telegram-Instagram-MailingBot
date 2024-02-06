import asyncio
import random
import uvloop
from selenium.common.exceptions import TimeoutException

from App.Database.DAL.AccountInstDAL import AccountInstDAL
from App.Database.session import async_session
from App.Parser.InstagramParser import InstagramParser, InstagramParserExceptions
import aioschedule

async def sleep():
    asyncio.sleep(10)

async def mainLayer():
    async with async_session() as session:
        instagramParserExceptions = InstagramParserExceptions()
        account_inst_dal = AccountInstDAL(session)

        uvloop.install()

        while True:
            accounts = await account_inst_dal.getSessionNamesWithTrueStatus()

            instagramParsers = [InstagramParser(login=account_name, password="") for account_name in accounts]

            for instagramParser in instagramParsers:
                account = await account_inst_dal.getAccountBySessionName(instagramParser.login)
                if account and account.target_channels:
                    followers = await account_inst_dal.getFollowers(account_inst_id=account.id)
                    for follower in followers:
                        result = await instagramParser.async_send_message(
                            message = account.message,
                            channel = follower
                        )
                        if (result == instagramParserExceptions.PrivateAccount):
                            pass
                        if (isinstance(result, TimeoutException)):
                            pass

                        delay = random.randint(5, 10)
                        print(f"delay: {delay} for account: {instagramParser.login}")
                        aioschedule.every(1).to(delay).seconds.do(sleep)
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(mainLayer())
