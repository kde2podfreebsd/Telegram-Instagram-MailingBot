import os

from App.Config.bot import bot


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sessions_dirPath = os.path.join(basedir, "UserAgent", "sessions")
inst_sessions_dirPath = os.path.join(basedir, "Parser", "sessions")
pfp_file_path = "/Users/user/Spam-Tg-Inst-Service/me.jpg"
logs_dirPath = f"{basedir}/Logger/logs"


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class MessageContextManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.help_menu_msgId_to_delete = {}

    async def add_msgId_to_help_menu_dict(self, chat_id, msgId):
        self.help_menu_msgId_to_delete[chat_id] = msgId

    async def delete_msgId_from_help_menu_dict(self, chat_id):
        if self.help_menu_msgId_to_delete[chat_id] is not None:
            await bot.delete_message(chat_id, self.help_menu_msgId_to_delete[chat_id])
            self.help_menu_msgId_to_delete[chat_id] = None


@singleton
class AccountContext:
    def __init__(self):
        self.account_name = {}

    def updateAccountName(self, chat_id: int, account_name: str):
        self.account_name[chat_id] = account_name

@singleton
class LoginContext:
    def __init__(self):
        self.login = {}

    def updateLogin(self, chat_id: int, login: str):
        self.login[chat_id] = login

message_context_manager = MessageContextManager()
account_context = AccountContext()
login_context = LoginContext()
