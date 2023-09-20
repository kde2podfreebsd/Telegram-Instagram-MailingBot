import asyncio
import random

import uvloop

from App.Config import singleton
from App.Database.DAL.AccountDAL import AccountDAL
from App.Database.session import async_session
from App.UserAgent.Core.UserAgentCore import UserAgentCore


@singleton
class MessageTracker:
    def __init__(self):
        self.message_ids = {}

    def record_message(self, session_name, chat, message_id):
        if session_name not in self.message_ids:
            self.message_ids[session_name] = {}
        self.message_ids[session_name][chat] = message_id

    def get_last_message_id(self, session_name, chat):
        return self.message_ids.get(session_name, {}).get(chat, None)

    def clear_last_message_id(self, session_name, chat):
        if session_name in self.message_ids and chat in self.message_ids[session_name]:
            del self.message_ids[session_name][chat]


async def send_message(user_agent_core, chat, message, delay):
    tracker = MessageTracker()

    await user_agent_core.joinChat(chat)
    await asyncio.sleep(delay)

    last_message_id = tracker.get_last_message_id(user_agent_core.session_name, chat)
    if last_message_id:
        await user_agent_core.deleteMsg(chat, last_message_id)
        tracker.clear_last_message_id(user_agent_core.session_name, chat)

    response = await user_agent_core.sendMsg(chat, message)
    tracker.record_message(user_agent_core.session_name, chat, response["msg_ids"])


async def main():
    async with async_session() as session:
        uvloop.install()
        account_dal = AccountDAL(session)

        while True:
            accounts = await account_dal.getSessionNamesWithTrueStatus()
            userAgent_clients = [UserAgentCore(x) for x in accounts]

            tasks = []
            for client in userAgent_clients:
                account = await account_dal.getAccountBySessionName(client.session_name)
                if account and account.advertising_channels:
                    for channel in account.advertising_channels:
                        message = account.message
                        delay = random.uniform(1, 3)
                        task = asyncio.create_task(
                            send_message(client, channel, message, delay)
                        )
                        tasks.append(task)

            await asyncio.gather(*tasks)
            await asyncio.sleep(15)


if __name__ == "__main__":
    asyncio.run(main())
