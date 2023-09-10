import errno
import json
import logging
import os
import re
from typing import List

from App.Config import basedir
from App.Config import sessions_dirPath
from App.Logger import ApplicationLogger
from App.UserAgent.Configurator import AppConfig
from App.UserAgent.Configurator import ChannelConfig
from App.UserAgent.Configurator import ConfigValidationException
from App.UserAgent.Configurator import UserAgentConfig


class UserAgentConfigurator:
    logger = ApplicationLogger(log_level=logging.DEBUG)

    def __init__(self, channelCount: int):
        self.config_path = os.path.join(basedir, "Config", "UserAgents_config.json")

        if not os.path.exists(self.config_path):
            self.createConfigTemplate(channelCount)

    @logger.exception_handler
    def createConfigTemplate(self, channelCount: int):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        channels_config = []
        for i in range(1, channelCount + 1):
            channel = ChannelConfig(
                advertising_channel=f"@name{i}",
                target_chats=[f"@chat{j}" for j in range(1, 4)],
                tg_accounts=[f"session{j}.session" for j in range(1, 4)],
                advertising_messages=[f"Message{j}!" for j in range(1, 4)],
            )
            channels_config.append(channel)

        user_agent_config = UserAgentConfig(
            param1="value1", param2="value2", param3="value3"
        )

        config_data = AppConfig(
            channels_config=channels_config, userAgent_config=user_agent_config
        )

        with open(self.config_path, "w") as file:
            json.dump(config_data.to_dict(), file, indent=4)

    @logger.exception_handler
    def load_config(self) -> AppConfig:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), self.config_path
            )

        with open(self.config_path, "r") as file:
            config_data = json.load(file)
            if (
                "channels_config" not in config_data
                or "userAgent_config" not in config_data
            ):
                raise ValueError(
                    "Недопустимый файл конфигурации. Отсутствуют обязательные ключи."
                )

            channels_config = [
                ChannelConfig(**channel) for channel in config_data["channels_config"]
            ]
            user_agent_config = UserAgentConfig(**config_data["userAgent_config"])

            return AppConfig(
                channels_config=channels_config, userAgent_config=user_agent_config
            )

    @logger.exception_handler
    def update_config(
        self,
        new_channels_config: List[ChannelConfig],
        new_user_agent_config: UserAgentConfig,
    ):
        current_config = self.load_config()

        if current_config:
            if self.validate_channels_config(new_channels_config):
                current_config.channels_config = new_channels_config
            else:
                raise ConfigValidationException(
                    "Недопустимая конфигурация каналов.", "channels_config", 0
                )

            if self.validate_user_agent_config(new_user_agent_config):
                current_config.userAgent_config = new_user_agent_config
            else:
                raise ConfigValidationException(
                    "Недопустимая конфигурация юзер-агента.", "userAgent_config", 0
                )

            with open(self.config_path, "w") as file:
                json.dump(current_config.to_dict(), file, indent=4)
        else:
            config_data = AppConfig(
                channels_config=new_channels_config,
                userAgent_config=new_user_agent_config,
            )

            with open(self.config_path, "w") as file:
                json.dump(config_data.to_dict(), file, indent=4)

        self.logger.log_info("App.Config.UserAgents_config Update!")

    @logger.exception_handler
    def validate_channels_config(self, channels_config: List[ChannelConfig]) -> bool:
        for channel_index, channel in enumerate(channels_config):
            if not self.validate_advertising_channel(channel.advertising_channel):
                raise ConfigValidationException(
                    f"Недопустимый формат advertising_channel для канала с индексом {channel_index}.",
                    "channels_config",
                    channel_index,
                )
            if not all(
                self.validate_advertising_channel(chat) for chat in channel.target_chats
            ):
                raise ConfigValidationException(
                    f"Недопустимый формат target_chats для канала с индексом {channel_index}.",
                    "channels_config",
                    channel_index,
                )

        for channel_index, channel in enumerate(channels_config):
            for account_index, account in enumerate(channel.tg_accounts):
                if not account.endswith(".session"):
                    raise ConfigValidationException(
                        f"Недопустимый формат tg_account для аккаунта с индексом {account_index} в канале с индексом {channel_index}. Должно оканчиваться на '.session'.",
                        "channels_config",
                        channel_index,
                    )

                account_path = os.path.join(sessions_dirPath, account)
                if not os.path.exists(account_path):
                    raise ConfigValidationException(
                        f"Файл для tg_account с индексом {account_index} в канале с индексом {channel_index} не существует: {account}.",
                        "channels_config",
                        channel_index,
                    )

        for channel_index, channel in enumerate(channels_config):
            for message_index, message in enumerate(channel.advertising_messages):
                if not isinstance(message, str):
                    raise ConfigValidationException(
                        f"Недопустимый формат advertising_messages для сообщения с индексом {message_index} в канале с индексом {channel_index}.",
                        "channels_config",
                        channel_index,
                    )

        return True

    @staticmethod
    @logger.exception_handler
    def validate_advertising_channel(channel: str) -> bool:
        valid_formats = [r"^https://t.me/\w+$", r"^@[\w_]+$", r"^t.me/\w+$"]
        for pattern in valid_formats:
            if re.match(pattern, channel):
                return True
        return False

    @staticmethod
    @logger.exception_handler
    def validate_user_agent_config(user_agent_config: UserAgentConfig) -> bool:
        for attr_value in user_agent_config.__dict__.values():
            if not isinstance(attr_value, str):
                return False
        return True


if __name__ == "__main__":
    configurator = UserAgentConfigurator(channelCount=2)

    new_channels_config = [
        ChannelConfig(
            advertising_channel="@new_channel",
            target_chats=["@new_chat1", "@new_chat2"],
            tg_accounts=["session_new.session"],
            advertising_messages=["New Message!"],
        ),
        ChannelConfig(
            advertising_channel="https://t.me/publicgrouptesttest",
            target_chats=["@new_chat3", "t.me/publicgrouptesttest"],
            tg_accounts=["session_new.session"],
            advertising_messages=["New Message!"],
        ),
        ChannelConfig(
            advertising_channel="@new_channel",
            target_chats=["@new_chat1", "@new_chat2"],
            tg_accounts=["session_new.session"],
            advertising_messages=["New Message!"],
        ),
        ChannelConfig(
            advertising_channel="https://t.me/publicgrouptesttest",
            target_chats=["@new_chat3", "t.me/publicgrouptesttest"],
            tg_accounts=["session_new.session"],
            advertising_messages=["New Message!"],
        ),
    ]

    new_user_agent_config = UserAgentConfig(
        param1="new_value1", param2="new_value2", param3="new_value3"
    )

    try:
        configurator.update_config(new_channels_config, new_user_agent_config)
    except ConfigValidationException as e:
        print(e)
