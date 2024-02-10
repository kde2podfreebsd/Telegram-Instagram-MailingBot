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
        await update_premium_members_db(
            account_stories_dal=account_stories_dal
        )
        while True:
            accounts_session_names = await account_stories_dal.getSessionNamesWithTrueStatus()
            user_agent_clients = [UserAgentCore(session_name) for session_name in accounts_session_names]
            tasks = []
            for client in user_agent_clients:
                account = await account_stories_dal.getAccountBySessionName(session_name=client.session_name)
                premium_members = []
                for premium_member in premium_members_db:
                    if (premium_member["id"] == account.id):
                        premium_members.append(premium_member["username"])

                task = coro_give_reaction(client=client, usernames=premium_members)
                tasks.append(task)
  
                
            asyncio.gather(*tasks)
            await asyncio.sleep(60)  

async def coro_give_reaction(client: UserAgentCore, usernames: list):
    await client.giveReaction(usernames)

async def update_premium_members_db(account_stories_dal: AccountStoriesDAL):
    global premium_members_db
    premium_members_db = await account_stories_dal.getAllChatMembers()

if __name__ == "__main__":
    asyncio.run(mainLayer())