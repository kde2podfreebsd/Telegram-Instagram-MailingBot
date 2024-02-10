import asyncio
import random

import uvloop

from App.Config import singleton
from App.Database.DAL.AccountTgDAL import AccountDAL
from App.Database.session import async_session
from App.UserAgent.Core.UserAgentCore import UserAgentCore
import aioschedule


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


async def sleep():
    asyncio.sleep(10)

async def mainLayer():
    async with async_session() as session:
        account_dal = AccountDAL(session)
        message_tracker = MessageTracker()

        uvloop.install()

        while True:
            accounts = await account_dal.getSessionNamesWithTrueStatus()

            userAgent_clients = [UserAgentCore(x) for x in accounts]

            tasks = []
            for client in userAgent_clients:
                account = await account_dal.getAccountBySessionName(client.session_name)
                if account and account.advertising_channels:
                    for chats in account.advertising_channels:
                        last_message_id = message_tracker.get_last_message_id(client.session_name, chats)
                        if last_message_id:
                            await client.deleteMsg(chat=chats, message_ids=last_message_id)
                            message_tracker.clear_last_message_id(client.session_name, chats)

                        msg = await client.sendMsg(chat=chats, message=account.message)

                        message_tracker.record_message(client.session_name, chats, msg['msg_ids'])

                        print(msg)

                        delay = random.randint(5, 10)
                        print(f"delay: {delay} for account: {client.session_name}")
                        aioschedule.every(1).to(delay).seconds.do(sleep)
            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(mainLayer())
