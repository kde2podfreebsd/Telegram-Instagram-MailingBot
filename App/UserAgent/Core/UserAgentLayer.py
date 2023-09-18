import asyncio
import random

import uvloop

from App.Database.DAL.AccountDAL import AccountDAL
from App.Database.session import async_session
from App.UserAgent.Core.UserAgentCore import UserAgentCore


async def send_message(user_agent_core, chat, message, delay):
    await user_agent_core.joinChat(chat)
    await asyncio.sleep(delay)
    await user_agent_core.sendMsg(chat, message)


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
                        delay = random.uniform(10, 15)
                        task = asyncio.create_task(
                            send_message(client, channel, message, delay)
                        )
                        tasks.append(task)

            await asyncio.gather(*tasks)
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
