from abc import ABCMeta
from abc import abstractmethod
from abc import abstractstaticmethod
from typing import Optional
from typing import Union

from pyrogram import enums


class UserAgentCoreInterface(metaclass=ABCMeta):
    @abstractmethod
    async def get_me(self):
        """
        Implement get_me function
        :return:
        """

    @abstractmethod
    async def joinChat(self, chat: Union[str | int]):
        """
        Implement join chat function
        :param chat:
        :return:
        """

    @abstractmethod
    async def leftChat(self, chat: Union[str | int]):
        """
        Implement left chat function
        :param chat:
        :return:
        """

    @abstractstaticmethod
    async def create_session(
        session_name: str, api_id: int, api_hash: str, sleep_threshold: int
    ):
        """
        Implement create .session file for telegram account
        :param session_name:
        :param api_id:
        :param api_hash:
        :param sleep_threshold:
        :return:
        """

    @abstractmethod
    async def send_message(
        self,
        chat: Union[str | int],
        message: str,
        parse_mode: Optional[enums.ParseMode] = None,
    ):
        """
        Implement send message to chat
        :param parse_mode:
        :param chat:
        :param message:
        :return:
        """

    @abstractmethod
    def synchronize_chats(self):
        """
        Implement synchronize chats with the config
        :return:
        """
