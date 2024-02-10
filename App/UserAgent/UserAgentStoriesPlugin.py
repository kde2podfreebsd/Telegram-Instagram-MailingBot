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
                account = await account_stories_dal.getAccountBySessionName(session_name=client.session_name)
                premium_members = await account_stories_dal.getPremiumMemebers(
                    account_stories_id=account.id
                )
                aioschedule.every(0).to(account.delay).minutes.do(
                    give_reaction_wrapper, client, premium_members
                )

            await asyncio.sleep(10)  

def give_reaction_wrapper(client, premium_members):
    async def wrapped():
        await client.giveReaction(usernames=premium_members)
    return wrapped

if __name__ == "__main__":
    asyncio.run(mainLayer())