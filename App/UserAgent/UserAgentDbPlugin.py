from App.Database.DAL.AccountTgDAL import AccountDAL
from App.Database.session import async_session
from App.UserAgent.Core.UserAgentCore import UserAgentCore
import asyncio

async def get_members_from_tg(session_name, usernames, limit=None):
    UserAgent = UserAgentCore(session_name=session_name)
    async with UserAgent.app as client:
        db = []
        for username in usernames:
            total_members = []
            async for participant in client.iter_participants(username, limit=limit):
                total_members.append(participant)
            for member in total_members:
                if member.username and member.premium:
                    db.append([
                        member.first_name,
                        member.last_name,
                        member.username,
                        member.premium
                    ])
    return db


if __name__ == "__main__":
    db = asyncio.run(get_members_from_tg("2", ["MafiaSchool21"]))
    print(db)


