import asyncio
# from typing import Optional

import uvloop
from telethon import TelegramClient
# import pyrogram

from App.Config import sessions_dirPath
from App.Logger import ApplicationLogger


logger = ApplicationLogger()


class UserAgentCore:
    def __init__(self, session_name: str):
        self.session_name = session_name
        self.app = TelegramClient(f"{sessions_dirPath}/{session_name}", api_id=123, api_hash="123")
        logger.log_info(
            f"Init UserAgentCore on {session_name} session. Path to session {sessions_dirPath}/{session_name}"
        )

    @classmethod
    @logger.exception_handler
    async def createSession(cls, session_name: str, api_id: int, api_hash: str):
        async with TelegramClient(
            f"{sessions_dirPath}/{session_name}", api_id, api_hash
        ) as app:
            await app.send_message("me", f"init session {session_name}")
            logger.log_info(
                f"Create session {session_name} in path: {sessions_dirPath}/{session_name}"
            )

    @logger.exception_handler
    async def sendMsg(
        self,
        chat: str | int,
        message: str,
        # parseMode: Optional[
        #     pyrogram.enums.ParseMode
        # ] = pyrogram.enums.ParseMode.MARKDOWN,
        parseMode='md',
    ):
        async with self.app as app:
            output = await app.send_message(
                chat, message, parse_mode=parseMode
            )
            logger.log_info(f"Send message to: {chat}. Message: {message}")
            return {"msg_ids": output.id, "chat": chat}

    @logger.exception_handler
    async def deleteMsg(self, chat: str | int, message_ids: int):
        async with self.app as app:
            await app.delete_messages(chat_id=chat, message_ids=message_ids)
            logger.log_info(f"Deleted message from: {chat}. Message: {message_ids}")

    @logger.exception_handler
    async def joinChat(self, chat: str | int):
        async with self.app as app:
            await app.join_chat(chat)
            logger.log_info(f"Join in chat: {chat}")

    @logger.exception_handler
    async def leaveChat(self, chat: str | int):
        async with self.app as app:
            await app.leave_chat(chat)
            logger.log_info(f"Leave from chat: {chat}")

    @logger.exception_handler
    async def getMe(self):
        async with self.app as app:
            logger.log_info(
                f"Get info about account registered by {self.session_name} session"
            )
            return await app.get_me()


# if __name__ == "__main__":
#     uvloop.install()
#
#     asyncio.run(UserAgentCore.createSession(
#         session_name="session",
#         api_id=,
#         api_hash=""
#     ))


#----------unnecessary-------------
    # u = UserAgentCore("rhdv")
    # u1 = UserAgentCore("complicat9d")
    # asyncio.run(u1.sendMsg(chat="@complicat9d", message="test1", parseMode=pyrogram.enums.ParseMode.MARKDOWN))
    # asyncio.run(
    #     u1.sendMsg(chat="@bubblesortdudoser", message="test1", parseMode=pyrogram.enums.ParseMode.MARKDOWN))
    
    # asyncio.run(u.joinChat("@publicgrouptesttest"))
    # asyncio.run(u.leaveChat("@publicgrouptesttest"))
    # asyncio.run(u.getMe())
