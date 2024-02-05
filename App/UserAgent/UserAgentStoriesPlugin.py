import asyncio
import uvloop
import aioschedule

from App.Database.DAL.AccountStoriesDAL import AccountStoriesDAL
from App.Database.session import async_session
from App.UserAgent.Core.UserAgentCore import UserAgentCore

async def mainLayer():
    async with async_session() as session:
        account_stories_dal = AccountStoriesDAL(session)
        uvloop.install()

        while True:
            accounts_session_names = await account_stories_dal.getSessionNamesWithTrueStatus()
            user_agent_clients = [UserAgentCore(session_name) for session_name in accounts_session_names]

            for client in user_agent_clients:
                asyncio.create_task(schedule_reaction(client, account_stories_dal))

            await asyncio.sleep(60)  # Ждем 60 секунд перед повторной итерацией

async def schedule_reaction(client, account_stories_dal):
    account = await account_stories_dal.getAccountBySessionName(client.session_name)
    delay = account.delay
    usernames_job = aioschedule.every().day.do(update_usernames, account_stories_dal, account)

    if account:
        aioschedule.every(delay).minutes.do(client.giveReaction, usernames_job)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def update_usernames(account_stories_dal, account):
    await account_stories_dal.getPremiumMemebers(account.id)
   


if __name__ == "__main__":
    asyncio.run(mainLayer())
