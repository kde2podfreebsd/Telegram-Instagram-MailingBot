# import asyncio
# import random

# import uvloop

# from App.Config import singleton
# from App.Database.DAL.AccountStoriesDAL import AccountStoriesDAL
# from App.Database.session import async_session
# from App.UserAgent.Core.UserAgentCore import UserAgentCore
# import aioschedule

# async def mainLayer():
#     async with async_session() as session:
#         account_stories_dal = AccountStoriesDAL(session)
        



#         uvloop.install()

#         while True:
#             accounts = await account_dal.getSessionNamesWithTrueStatus()

#             userAgent_clients = [UserAgentCore(x) for x in accounts]

#             tasks = []
#             for client in userAgent_clients:
#                 account = await account_dal.getAccountBySessionName(client.session_name)
#                 if account and account.advertising_channels:
#                     for chats in account.advertising_channels:
#                         last_message_id = message_tracker.get_last_message_id(client.session_name, chats)
#                         if last_message_id:
#                             await client.deleteMsg(chat=chats, message_ids=last_message_id)
#                             message_tracker.clear_last_message_id(client.session_name, chats)

#                         msg = await client.sendMsg(chat=chats, message=account.message)

#                         message_tracker.record_message(client.session_name, chats, msg['msg_ids'])

#                         print(msg)

#                         delay = random.randint(5, 10)
#                         print(f"delay: {delay} for account: {client.session_name}")
#                         aioschedule.every(1).to(delay).seconds.do(sleep)
#             await asyncio.sleep(10)


# if __name__ == "__main__":
#     asyncio.run(mainLayer())
