import pytest
from App.UserAgent.Configurator.ConfiguratorEntities import ChannelConfig, UserAgentConfig, AppConfig, ConfigValidationException

# Тесты для класса ChannelConfig
def test_channel_config_creation():
    config = ChannelConfig("channel1", ["chat1", "chat2"], ["account1"], ["message1", "message2"])
    assert config.advertising_channel == "channel1"
    assert config.target_chats == ["chat1", "chat2"]
    assert config.tg_accounts == ["account1"]
    assert config.advertising_messages == ["message1", "message2"]

def test_channel_config_to_dict():
    config = ChannelConfig("channel1", ["chat1", "chat2"], ["account1"], ["message1", "message2"])
    expected_dict = {
        "advertising_channel": "channel1",
        "target_chats": ["chat1", "chat2"],
        "tg_accounts": ["account1"],
        "advertising_messages": ["message1", "message2"]
    }
    assert config.to_dict() == expected_dict

# Тесты для класса UserAgentConfig
def test_user_agent_config_creation():
    config = UserAgentConfig("param1", "param2", "param3")
    assert config.param1 == "param1"
    assert config.param2 == "param2"
    assert config.param3 == "param3"

def test_user_agent_config_to_dict():
    config = UserAgentConfig("param1", "param2", "param3")
    expected_dict = {
        "param1": "param1",
        "param2": "param2",
        "param3": "param3"
    }
    assert config.to_dict() == expected_dict

# Тесты для класса AppConfig
def test_app_config_creation():
    channel1 = ChannelConfig("channel1", ["chat1", "chat2"], ["account1"], ["message1", "message2"])
    channel2 = ChannelConfig("channel2", ["chat3"], ["account2"], ["message3"])
    user_agent = UserAgentConfig("param1", "param2", "param3")
    config = AppConfig([channel1, channel2], user_agent)
    assert config.channels_config == [channel1, channel2]
    assert config.userAgent_config == user_agent

def test_app_config_to_dict():
    channel1 = ChannelConfig("channel1", ["chat1", "chat2"], ["account1"], ["message1", "message2"])
    channel2 = ChannelConfig("channel2", ["chat3"], ["account2"], ["message3"])
    user_agent = UserAgentConfig("param1", "param2", "param3")
    config = AppConfig([channel1, channel2], user_agent)
    expected_dict = {
        "channels_config": [
            {
                "advertising_channel": "channel1",
                "target_chats": ["chat1", "chat2"],
                "tg_accounts": ["account1"],
                "advertising_messages": ["message1", "message2"]
            },
            {
                "advertising_channel": "channel2",
                "target_chats": ["chat3"],
                "tg_accounts": ["account2"],
                "advertising_messages": ["message3"]
            }
        ],
        "userAgent_config": {
            "param1": "param1",
            "param2": "param2",
            "param3": "param3"
        }
    }
    assert config.to_dict() == expected_dict

# Тест для класса ConfigValidationException
def test_config_validation_exception():
    exception = ConfigValidationException("field1", 0, "Invalid value")
    assert str(exception) == "Ошибка конфигурации: Поле 'field1' в индексе 0 недопустимо."

if __name__ == "__main__":
    pytest.main()
