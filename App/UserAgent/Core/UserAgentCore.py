from typing import Optional
from typing import Union

from pyrogram import Client
from pyrogram import enums

from App.Config import sessions_dirPath
from App.UserAgent.Core.UserAgentCoreInterface import UserAgentCoreInterface


class UserAgentCore(UserAgentCoreInterface):
    def __init__(self, session_name: str):

        self.app = Client(f"{sessions_dirPath}/{session_name}")

    @staticmethod
    async def create_session(
        session_name: str, api_id: int, api_hash: str, sleep_threshold: int
    ):
        async with Client(
            name=f"{sessions_dirPath}/{session_name}",
            api_id=api_id,
            api_hash=api_hash,
            sleep_threshold=sleep_threshold,
        ) as app:
            await app.send_message(
                "me", "Init account session from Auto-dispatchTG application"
            )

    async def get_me(self):
        async with self.app as app:
            await app.get_me()

    async def joinChat(self, chat: Union[str | int]):
        async with self.app as app:
            await app.join_chat(chat)

    async def leftChat(self, chat: Union[str | int]):
        async with self.app as app:
            await app.leave_chat(chat)

    async def send_message(
        self,
        chat: Union[str | int],
        message: str,
        parse_mode: Optional[enums.ParseMode] = None,
    ):
        async with self.app as app:
            await app.send_message(chat_id=chat, text=message, parse_mode=parse_mode)
