from App.UserAgent.Core.UserAgentCore import UserAgentCore

from App.Logger import ApplicationLogger

import asyncio

logger = ApplicationLogger()

class DbPremiumUsersExceptions():
    def __init__(self, username):
        self.WRONG_USERNAME_EXCEPTION=f"No user has \"{username}\" as username"
        self.ADMIN_PRIVILEGES_EXCEPTION="Chat admin privileges are required to do that in the specified chat (for example, to send a message in a channel which is not yours), or invalid permissions used for the channel or group (caused by GetParticipantsRequest)"

    
@logger.exception_handler
async def get_members_from_tg(session_name, usernames, limit=None):
    UserAgent = UserAgentCore(session_name=session_name)
    async with UserAgent.app as client:
        db = []
        for username in usernames:
            async for participant in client.iter_participants(username, limit=limit):
                if participant.username and participant.premium:
                    db.append(participant.username)
            return db



if __name__ == "__main__":
    db = asyncio.run(get_members_from_tg("test", ["MafiaSchool21"]))
    print(db)


