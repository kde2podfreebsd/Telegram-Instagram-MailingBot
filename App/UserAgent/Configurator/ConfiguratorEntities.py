from dataclasses import dataclass
from typing import List


@dataclass
class ChannelConfig:
    advertising_channel: str
    target_chats: List[str]
    tg_accounts: List[str]
    advertising_messages: List[str]

    def to_dict(self) -> dict:
        return {
            "advertising_channel": self.advertising_channel,
            "target_chats": self.target_chats,
            "tg_accounts": self.tg_accounts,
            "advertising_messages": self.advertising_messages,
        }


@dataclass
class UserAgentConfig:
    param1: str
    param2: str
    param3: str

    def to_dict(self) -> dict:
        return {"param1": self.param1, "param2": self.param2, "param3": self.param3}


@dataclass
class AppConfig:
    channels_config: List[ChannelConfig]
    userAgent_config: UserAgentConfig

    def to_dict(self) -> dict:
        return {
            "channels_config": [channel.to_dict() for channel in self.channels_config],
            "userAgent_config": self.userAgent_config.to_dict(),
        }


class ConfigValidationException(Exception):
    def __init__(self, field: str, index: int, message: str):
        self.message = message
        self.field = field
        self.index = index
        super().__init__(self.message)

    def __str__(self):
        return f"Ошибка конфигурации: Поле '{self.field}' в индексе {self.index} недопустимо."
