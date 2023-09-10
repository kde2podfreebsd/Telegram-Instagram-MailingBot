import pytest

from App.UserAgent.Configurator import ChannelConfig
from App.UserAgent.Configurator import UserAgentConfig
from App.UserAgent.Configurator import UserAgentConfigurator

# from App.UserAgent.Configurator import ConfigValidationException


@pytest.fixture
def configurator(tmp_path):
    # Создаем временный файл конфигурации
    temp_config_path = tmp_path / "test_temp_config.json"
    return UserAgentConfigurator(channelCount=2), temp_config_path


def test_create_config_template(configurator, tmp_path):
    configurator, temp_config_path = configurator
    # Создаем корректный шаблон конфигурации
    configurator.createConfigTemplate(2)


def test_load_config(configurator):
    configurator, _ = configurator
    # Проверяем, что конфигурация может быть загружена
    configurator.load_config()


def test_validate_channels_config(configurator):
    configurator, _ = configurator
    # Проверяем валидацию конфигурации каналов с недопустимой конфигурацией
    invalid_channels_config = [
        ChannelConfig(
            advertising_channel="invalid_channel",
            target_chats=["invalid_chat"],
            tg_accounts=["invalid_account"],
            advertising_messages=[
                "Invalid Message"
            ],  # Непустое, но недопустимое сообщение
        )
    ]

    configurator.validate_channels_config(invalid_channels_config)


def test_validate_user_agent_config(configurator):
    configurator, _ = configurator
    # Проверяем валидацию конфигурации юзер-агента с недопустимой конфигурацией
    invalid_user_agent_config = UserAgentConfig(
        param1="new_value1", param2="new_value2", param3="new_value3"
    )

    configurator.validate_user_agent_config(invalid_user_agent_config)
