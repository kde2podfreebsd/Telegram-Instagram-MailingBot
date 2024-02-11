import asyncio
import os

from telethon.tl.types import InputMediaPhoto 
from telebot import formatting
from telebot import types

from App.Database.DAL.AccountTgDAL import AccountDAL
from App.Database.DAL.AccountStoriesDAL import AccountStoriesDAL
from App.Database.DAL.AccountInstDAL import AccountInstDAL
from App.Database.DAL.ProxyDAL import ProxyAddressDAL
from App.Database.session import async_session

from App.UserAgent.Core import UserAgentCore

from App.Config import REDQUIRED_AMOUNT_OF_PROXIES

class MarkupBuilder(object):

    _change_status = None
    _adv_chat_added = None
    _sendAddAdvChatText = None
    _errorSetTargetChannel = None
    _prompt_edited: object = None
    _sendChangePromptText: object = None
    _message_edited: object = None
    _sendChangeAccountMessageText: object = None
    _changeAccountMsg: object = None
    _editAccountsMenuText: object = None
    _new_account_state1: object = None
    _hide_menu: object = None
    _welcome_text: object = None

    _change_aiosheduler_status = None
    _error_username_floodWait = None
    _launch_stories_text = None
    _change_status_account_inst = None
    _error_insufficient_amount_of_proxies = None


    @classmethod
    async def AccountListKeyboard(cls):
        async with async_session() as session:
            account_dal = AccountDAL(session)
            acc_out = await account_dal.getAllAccounts()
            ACCOUNTS = [
                {
                    "session_name": os.path.splitext(
                        os.path.basename(x.session_file_path)
                    )[0]
                }
                for x in acc_out
            ]

            mp = types.InlineKeyboardMarkup(row_width=2)

            for account in ACCOUNTS:
                mp.add(
                    types.InlineKeyboardButton(
                        text=account["session_name"],
                        callback_data=f"edit_account#{account['session_name']}",
                    )
                )

            mp.add(
                types.InlineKeyboardButton(
                    text="🔙Назад", callback_data="back_to_spam_tg"
                )
            )

            return mp

    @classmethod 
    def AccountListServices(cls):
        return types.InlineKeyboardMarkup(
            row_width=2,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        "📝Спам рассылка телеграма",
                        callback_data="spam_tg"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "📷Спам рассылка инстаграма",
                        callback_data="spam_inst"
                    )
                ]
            ]
        )
    
    @classmethod
    async def AccountListKeyboardVisCfg(cls):
        async with async_session() as session:
            account_dal = AccountDAL(session)
            acc_out = await account_dal.getAllAccounts()
            ACCOUNTS = [
                {
                    "session_name": os.path.splitext(
                        os.path.basename(x.session_file_path)
                    )[0]
                }
                for x in acc_out
            ]

            mp = types.InlineKeyboardMarkup(row_width=2)

            for account in ACCOUNTS:
                mp.add(
                    types.InlineKeyboardButton(
                        text=account["session_name"],
                        callback_data=f"viscfg_account#{account['session_name']}",
                    )
                )

            mp.add(
                types.InlineKeyboardButton(
                    text="🔙Назад", callback_data="back_to_spam_tg"
                )
            )

            return mp
    
    @classmethod
    async def AccountListKeyboardStroies(cls):
        async with async_session() as session:
            account_dal = AccountDAL(session)
            acc_out = await account_dal.getAllAccounts()
            ACCOUNTS = [
                {
                    "session_name": os.path.splitext(
                        os.path.basename(x.session_file_path)
                    )[0]
                }
                for x in acc_out
            ]

            mp = types.InlineKeyboardMarkup(row_width=2)

            for account in ACCOUNTS:
                mp.add(
                    types.InlineKeyboardButton(
                        text=account["session_name"],
                        callback_data=f"acc_stories#{account['session_name']}",
                    )
                )

            mp.add(
                types.InlineKeyboardButton(
                    text="🔙Назад", callback_data="back_to_spam_tg"
                )
            )

            return mp

    @classmethod 
    def SpamTgActionsList(cls):
        return types.InlineKeyboardMarkup(
            row_width=2,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        "🤖Добавить аккаунт",
                        callback_data="new_account_menu"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "🎨Визуальный конфиг аккаунта",
                        callback_data="vis_cfg"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "💬Настроить спам рассылку",
                        callback_data="acc_edit"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "🔎Просмотр сториз",
                        callback_data="stories_menu"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "🔙Назад",
                        callback_data="back_to_service_menu"
                    )
                ]
            ]
        )

    @classmethod
    def EditVisualOptions(cls, account_name):
        return types.InlineKeyboardMarkup(row_width=2,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        "Сменить фото профиля", 
                        callback_data=f"chng_pfp#{account_name}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "Поменять first_name", 
                        callback_data=f"chng_first_name#{account_name}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "Поменять last_name", 
                        callback_data=f"chng_last_name#{account_name}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "Поменять username", 
                        callback_data=f"chng_username#{account_name}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "Поменять описание аккаунта", 
                        callback_data=f"chng_profile_desc#{account_name}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "🔙Назад",
                        callback_data="back_to_vis_cfg"
                    )
                ]
            ]
        )
    
    @classmethod
    async def AccountStoriesListKeyboard(cls):
        async with async_session() as session:
            account_dal = AccountStoriesDAL(session)
            acc_out = await account_dal.getAllAccounts()
            ACCOUNTS = [
                {
                    "session_name": os.path.splitext(
                        os.path.basename(x.session_file_path)
                    )[0]
                }
                for x in acc_out
            ]

            mp = types.InlineKeyboardMarkup(row_width=2)

            for account in ACCOUNTS:
                mp.add(
                    types.InlineKeyboardButton(
                        text=account["session_name"],
                        callback_data=f"look_stories#{account['session_name']}",
                    )
                )

            mp.add(
                types.InlineKeyboardButton(
                    text="🔙Назад", callback_data="back_to_spam_tg"
                )
            )

            return mp

    @classmethod
    def StoriesMenu(cls, account_name):
        return types.InlineKeyboardMarkup(row_width=2,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        "🚀Запуск просмотра сториз", 
                        callback_data=f"stories_service#{account_name}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "👀Отслеживание сториз", 
                        callback_data=f"aiosheduler_stories#{account_name}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "➕Добавить аккаунт для парсинга премиум пользователей", 
                        callback_data=f"add_trgt_chnl#{account_name}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "➖Удалить аккаунт для парсинга премиум пользователей", 
                        callback_data=f"delete_trgt_chnl#{account_name}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "🔙Назад",
                        callback_data="back_to_stories_menu"
                    )
                ],
            ],
        )

    @classmethod
    async def showAccountStoriesActions(cls, account_name):
        async with async_session() as session:
            account_stories_dal = AccountStoriesDAL(session)
            account = await account_stories_dal.getAccountBySessionName(session_name=account_name)

            account_username = account.session_file_path.split("/")[-1].replace(".session", "")
            account_username = account_username.replace("_", "\\_")

            target_channels = ""
            if account.target_channels is not None:
                amount_of_target_channels = len(account.target_channels)
                for x in account.target_channels:
                    y = x.replace("_", "\\_") if "." in x else x
                    if (account.target_channels.index(x) != amount_of_target_channels - 1):
                        target_channels += f"{y}\n"
                    else:
                        target_channels += f"{y}"
            else:
                target_channels = "🤷‍♂️Нет чатов для парсинга"

            premium_chat_members = await account_stories_dal.getPremiumMemebers(
                account_stories_id=account.id
            )
            number_premium_chat_members = len(premium_chat_members)

            number_premium_chat_members_with_stories = await UserAgentCore(
                session_name=account_name
            ).numberOfActiveStories(premium_chat_members)

            accountStoriesActionsText = f"""
Аккаунт: {account_username}
🎯Таргетные каналы: 
------------------
{target_channels}
------------------
💎Количество премиум подписчиков: {number_premium_chat_members}
😎Количество премиум подписчиков с сториз: {number_premium_chat_members_with_stories}
"""

            def split_string(input_string, max_length=4000):
                result = []
                for i in range(0, len(input_string), max_length):
                    result.append(input_string[i : i + max_length])
                return result

            return split_string(accountStoriesActionsText)
    
    @classmethod
    async def showAccountStoriesAioschdeulerActions(cls, account_name):
        async with async_session() as session:
            account_stories_dal = AccountStoriesDAL(session)
            account = await account_stories_dal.getAccountBySessionName(session_name=account_name)

            account_username = account.session_file_path.split("/")[-1].replace(".session", "")
            account_username = account_username.replace("_", "\\_")

            accountStoriesActionsText = f"""
Аккаунт: {account_username}
Задержка в минутах: {account.delay}
Статус: {"Активен" if account.aioscheduler_status else "Не активен"}
"""

            def split_string(input_string, max_length=4000):
                result = []
                for i in range(0, len(input_string), max_length):
                    result.append(input_string[i : i + max_length])
                return result

            return split_string(accountStoriesActionsText)

    @classmethod
    def AioshedulerStoriesMenu(cls, account_name):
        return types.InlineKeyboardMarkup(row_width=2,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        "⏰Изменить задержку", 
                        callback_data=f"chng_delay#{account_name}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "🔛Изменить статус отслеживания сториз", 
                        callback_data=f"chng_status#{account_name}"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "🔙Назад",
                        callback_data=f"back_to_look_stories#{account_name}"
                    )
                ],
            ],
        )

    @classmethod
    def AccountEditActions(cls, account_name):
        return types.InlineKeyboardMarkup(
            row_width=3,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="💬Изменить сообщение",
                        callback_data=f"change_acc_msg#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="✍️Изменить prompt для ChatGPT",
                        callback_data=f"change_prompt#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="⏰Изменить задержку",
                        callback_data=f"change_delay#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="➕Добавить рекламный чат",
                        callback_data=f"add_adv_chat#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="➖Убрать рекламный чат",
                        callback_data=f"remove_adv_chat#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🎯Изменить целевой канал",
                        callback_data=f"change_target_channel#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🆙Изменить статус",
                        callback_data=f"change_status#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔄Обновить рекламное сообщение ChatGPT",
                        callback_data=f"reload_chatgpt_message#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🗑Удалить аккаунт",
                        callback_data=f"delete_account#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", 
                        callback_data="back_to_acc_edit"
                    )
                ],
            ],
        )

    @classmethod
    async def AccountEditActions_text(cls, account_name):
        async with async_session() as session:
            account_dal = AccountDAL(session)
            account = await account_dal.getAccountBySessionName(
                session_name=account_name
            )

            advertising_channels = ""
            if account.advertising_channels is not None:
                for x in account.advertising_channels:
                    y = x.replace("_", "\\_") if "_" in x else x
                    advertising_channels += f"{y}\n"
            else:
                advertising_channels = "🤷‍♂️Нет чатов для рекламы"

            target_chat = (
                account.target_chat.replace("_", "\\_")
                if "_" in account.target_chat
                else account.target_chat
            )
            account_username = (
                os.path.splitext(os.path.basename(account.session_file_path))[
                    0
                ].replace("_", "\\_")
                if "_"
                in os.path.splitext(os.path.basename(account.session_file_path))[0]
                else os.path.splitext(os.path.basename(account.session_file_path))[0]
            )
            prompt = (
                account.prompt.replace("_", "\\_")
                if "_" in account.prompt
                else account.prompt
            )

            out_message = f"""
🤖Аккаунт: {account_username}
🎯Целевой канал: {target_chat}
🆙Статус: {"Активен" if account.status else "Не активен"}
⏰Задержка в минутах: {account.delay}
✍️ChatGPT prompt:
-------------------
{prompt}
-------------------
💬Рекламное сообщение:
-------------------

{account.message}

-------------------
📝Чаты для рекламы:
{advertising_channels}
"""
            print(out_message[62])

            def split_string(input_string, max_length=4000):
                result = []
                for i in range(0, len(input_string), max_length):
                    result.append(input_string[i : i + max_length])
                return result

            return split_string(out_message)
    
    @classmethod
    @property
    def hide_menu(cls):
        cls._hide_menu: object = types.ReplyKeyboardRemove()
        return cls._hide_menu

    @classmethod
    @property
    def welcome_text(cls):
        cls._welcome_text: object = formatting.format_text(
            formatting.mbold(
                "👋Приветствую! Это бот для управления автоматизированной рассылкой в телеграмм и инстаграм."
            ),
            "🔢Выбери необходимый пункт меню",
            separator="\n",
        )
        return cls._welcome_text
    
    @classmethod
    def SpamInstActionsList(cls):
        return types.InlineKeyboardMarkup(
            row_width=2,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        "🚪Войти в аккаунт инстаграм",
                        callback_data="logging_in_inst"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "💬Настроить спам рассылку",
                        callback_data="inst_acc_edit"
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        "🔙Назад",
                        callback_data="back_to_service_menu"
                    )
                ]
            ]
        )
    
    @classmethod
    def AccountInstEditActions(cls, account_name):
        return types.InlineKeyboardMarkup(
            row_width=3,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="💬Изменить сообщение",
                        callback_data=f"change_acc_inst_msg#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="▶️Добавить ссылку на рилз",
                        callback_data=f"add_reels_link#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="⏰Изменить задержку",
                        callback_data=f"chng_inst_delay#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="➕Добавить прокси",
                        callback_data=f"add_proxy#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="➖Удалить прокси",
                        callback_data=f"delete_proxy#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="➕Добавить канал для парсинга фолловеров",
                        callback_data=f"add_target_chat#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="➖Убрать канал для парсинга фолловеров",
                        callback_data=f"remove_target_chat#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔛Изменить статус",
                        callback_data=f"chng_inst_status#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🗑Удалить аккаунт",
                        callback_data=f"delete_inst_account#{account_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", 
                        callback_data="back_to_inst_acc_edit"
                    )
                ],
            ],
        )



    @classmethod
    async def showAccountInstActions(cls, account_name):
        async with async_session() as session:
            account_inst_dal = AccountInstDAL(session)
            account = await account_inst_dal.getAccountBySessionName(session_name=account_name)
            
            account_username = account.session_file_path.split("/")[-1].replace(".cookies", "")
            account_username = account_username.replace("_", "\\_")

            target_channels = ""
            if account.target_channels is not None and account.target_channels != []:
                amount_of_target_channels = len(account.target_channels)
                for x in account.target_channels:
                    y = x.replace("_", "\\_") 
                    if (account.target_channels.index(x) != amount_of_target_channels - 1):
                        target_channels += f"{y}\n"
                    else:
                        target_channels += f"{y}"
            else:
                target_channels = "🤷‍♂️Нет каналов для рассылки"
            proxy_dal = ProxyAddressDAL(session)
            proxies = await proxy_dal.getProxyAddressById(
                account_inst_id=account.id
            )

            proxies_string = ""
            if proxies is not None and proxies != []:
                amount_of_proxies = len(proxies)
                for proxy in proxies:
                    _proxy = proxy.replace("_", "\\_")
                    if (proxies.index(proxy) != amount_of_proxies - 1):
                        proxies_string += f"{_proxy}\n"
                    else:
                        proxies_string += f"{_proxy}"
            else:
                proxies_string = "🤷‍♂️Нет прокси адресов"

            account_message = account.message.replace("_", "\\_")
            reels_link = account.reels_link.replace("_", "\\_")

            accountInstActionsText = f"""
🤖Аккаунт: {account_username}
🔛Статус: {"Активен" if account.status else "Не активен"}
⏰Задержка в минутах: {account.delay}
💾Прокси:
------------------------
{proxies_string}
------------------------
🎯Каналы для рассылки: 
------------------------
{target_channels}
------------------------
🔗Ссылка на рилз:
{reels_link}
💬Рекламное сообщение:
------------------------
{account_message}
"""

            def split_string(input_string, max_length=4000):
                result = []
                for i in range(0, len(input_string), max_length):
                    result.append(input_string[i : i + max_length])
                return result

            return split_string(accountInstActionsText)

    @classmethod
    async def AccountInstListKeyboard(cls):
        async with async_session() as session:
            account_inst_dal = AccountInstDAL(session)
            acc_out = await account_inst_dal.getAllAccounts()
            ACCOUNTS_INST = [
                {
                    "session_name": os.path.splitext(
                        os.path.basename(x.session_file_path)
                    )[0]
                }
                for x in acc_out
            ]
            mp = types.InlineKeyboardMarkup(row_width=2)

            for account in ACCOUNTS_INST:
                mp.add(
                    types.InlineKeyboardButton(
                        text=account["session_name"],
                        callback_data=f"edit_inst_account#{account['session_name']}",
                    )
                )

            mp.add(
                types.InlineKeyboardButton(
                    text="🔙Назад", callback_data="back_to_spam_inst"
                )
            )

            return mp

    @classmethod
    @property
    def instLoggingInSuccessfullyText(cls):
        cls.instLoggingInSuccessfullyText = "✅<b>Логин в аккаунт инстаграма произошел успешно</b>"
        return cls.instLoggingInSuccessfullyText
    
    @classmethod
    @property
    def loggingIn(cls):
        cls.loggingIn = "<i>Происходит логин в аккаунт инстаграм, ожидайте...</i>"
        return cls.loggingIn
    
    @classmethod
    @property
    def errorInstLoggingIn(cls):
        cls.errorInstLoggingIn = "❌<b>Произошла ошибка при логине в аккаунт инстаграма, выйдите в меню логина и введите логин и пароль еще раз</b>"
        return cls.errorInstLoggingIn
    
    @classmethod
    @property
    def errorIncorrectPasswordOrLogin(cls):
        cls.erorrIncorrectPasswordOrLogin = "❌<b>Вы ввели неверный пароль или логин, выйдите в меню логина и введите логин и пароль еще раз</b>"
        return cls.erorrIncorrectPasswordOrLogin
    
    @classmethod
    @property
    def errorSuspendedAccount(cls):
        cls.errorSuspendedAccount = "❌<b>Аккаунт, чьи логин и пароль вы ввели, забанен</b>"
        return cls.errorSuspendedAccount

    @classmethod
    @property
    def errorExpiredProxy(cls):
        cls.errorExpiredProxy = "❌<b>У введенного прокси адреса закончился срок годности, перейдите в меню рассылки инстаграм, чтобы повторить лоигн в аккаунт</b>"
        return cls.errorExpiredProxy
    
    @classmethod
    @property
    def errorExpiredProxyDb(cls):
        cls.errorExpiredProxyDb = "❌<b>У введенного прокси адреса закончился срок годности, попробуйте ввести другой, либо вернитесь в меню рассылки иистаграм</b>"
        return cls.errorExpiredProxyDb

    @classmethod
    @property
    def getInstAccountLogin(cls):
        cls.getInstAccountLogin = "<b>Введите логин от вашего аккаунта инстаграм:</b>"
        return cls.getInstAccountLogin

    @classmethod
    @property
    def getInstAccountPassword(cls):
        cls.getInstAccountPassword = "<b>Введите пароль от вашего аккаунта инстаграм:</b>"
        return cls.getInstAccountPassword
    
    @classmethod 
    @property 
    def getProxyAddress(cls):
        cls.getProxyAddress = "<b>Введите адрес прокси сервера по образцу: IP_ADDRESS:PORT:LOGIN:PASSWORD</b>"
        return cls.getProxyAddress 
    
    @classmethod 
    @property 
    def errorGetProxyAddress(cls):
        cls.errorGetProxyAddress = "❌<b>Введенный прокси адрес не подходит по образцу: IP_ADDRESS:PORT:LOGIN:PASSWORD.\n Перейдите в меню рассылки инстаграма или введите прокси еще раз</b>"
        return cls.errorGetProxyAddress 
    
    
    @classmethod
    @property
    def sendUpdateMessageInstText(cls):
        cls.sendUpdateMessageInstText = "✉️<b>Введите сообщение для рассылки другим пользователям инстаграм:</b>"
        return cls.sendUpdateMessageInstText
    
    @classmethod
    @property
    def updatedMessageInstText(cls):
        cls.updatedMessageInstText = "✅<b>Сообщение для рассылки было успешно изменено</b>"
        return cls.updatedMessageInstText
    
    @classmethod
    @property
    def sendAddTargetChannelText(cls):
        cls.sendAddTargetChannelText = "<b>Введите название канала для рассылки в виде username:</b>"
        return cls.sendAddTargetChannelText
    
    @classmethod
    @property
    def parsingFollowers(cls):
        cls.parsingFollowers = "<i>Происходит парсинг фолловеров канала инстаграм, ожидайте...</i>"
        return cls.parsingFollowers

    @classmethod
    @property
    def addedInstTargetChannel(cls):
        cls.addedInstTargetChannel = "✅<b>Канал для рассылки был успешно добавлен в базу данных</b>"
        return cls.addedInstTargetChannel
    
    @classmethod
    @property
    def errorTargetInstChat(cls):
        cls.errorTargetInstChat = "❌<b>Вы ввели неправильное название канала (username), попробуйте еще раз или вернитесь в меню настройки сториз</b>"
        return cls.errorTargetInstChat
    
    @classmethod
    @property
    def errorDbTargetInstChannel(cls):
        cls.errorDbTargetInstChannel = "<b>❌Произошла ошибка при добавлении канала для рассылки в базу данных, попробуйте еще раз или вернитесь в меню настройки рассылки</b>"
        return cls.errorDbTargetInstChannel
    
    @classmethod
    @property
    def errorDbNonExistentTargetInstChannel(cls):
        cls.errorDbNonExistentTargetInstChannel = "<b>❌Вы пытаетесь удалить канал, который не существует в базе данных, попробуйте еще раз или вернитесь в меню настройки рассылки инстаграм</b>"
        return cls.errorDbNonExistentTargetInstChannel

    @classmethod
    @property
    def errorUpdatingInstMessage(cls):
        cls.errorUpdatingInstMessage = "❌<b>Произошла ошибка при обновлении сообщения аккаунта инстаграм, аккаунт нет в базе данных</b>"
        return cls.errorUpdatingInstMessage
    
    @classmethod
    @property
    def errorPageNotFound(cls):
        cls.errorPageNotFound = "❌<b>Username пользователя, который вы ввели, является не валидным: нет такой страницы</b>"
        return cls.errorPageNotFound

    @classmethod
    @property
    def sendRemoveTargetChannelText(cls):
        cls.sendRemoveTargetChannelText = "<b>Введите название канала для рассылки, который хотите удалить, в виде username:</b>"
        return cls.sendRemoveTargetChannelText
    
    @classmethod
    @property
    def removedInstTargetChannel(cls):
        cls.removedInstTargetChannel = "✅<b>Канал для рассылки был успешно удален из базы данных</b>"
        return cls.removedInstTargetChannel
    
    @classmethod
    @property
    def errorTargetInstChannelRemoval(cls):
        cls.errorTargetInstChannelRemoval = "❌</b>Вы ввели неправильное название канала для удаления (username), попробуйте еще раз или вернитесь в меню настройки сториз </b>"
        return cls.errorTargetInstChannelRemoval

    @classmethod
    @property
    def sendDeleteAccountInstText(cls):
        cls.sendDeleteAccountInstText = "<b>Вы точно хотите удалить данный аккаунт? Введите ДА, ТОЧНО для подтверждения</b>"
        return cls.sendDeleteAccountInstText
    
    @classmethod
    @property
    def deletedAccountInst(cls):
        cls.deletedAccountInst = "✅<b>Аккаунт инстаграм был успешно удален из базы данных</b>"
        return cls.deletedAccountInst

    @classmethod
    @property
    def errorUnknownDeletionAccountCommand(cls):
        cls.errorUnknownDeletionAccountCommand = "❌<b>Вы ввели неизвестную команду для удаления аккаунта. Введите ДА, ТОЧНО еще раз или вернитесь в меню рассылки</b>"
        return cls.errorUnknownDeletionAccountCommand
    
    @classmethod
    @property
    def errorDbAccountInstRemoval(cls):
        cls.errorUnknownDeletionAccountCommand = "❌<b>Аккаунт, который вы хотите удалить, не существует в базе данных, перейдите в меню рассылки</b>"
        return cls.errorUnknownDeletionAccountCommand
    
    @classmethod
    @property
    def errorNoTargetInstChannels(cls):
        cls.errorNoTargetInstChannels =  "<b>❌Нет таргетных каналов инстаграм, из которых можно спарсить подписчиков.\n Добавьте их с помощью \"➕Добавить канал для парсинга фолловеров\"</b>"
        return cls.errorNoTargetInstChannels
    
    @classmethod
    @property
    def errorNoMessage(cls):
        cls.errorNoTargetInstChannels =  "<b>❌Нет сообщения для рассылки. Добавьте его с помощью \"💬Изменить сообщение\"</b>"
        return cls.errorNoTargetInstChannels
    
    @classmethod
    def errorInsufficientAmountOfProxies(cls, amount_of_proxies: int):
        cls._error_insufficient_amount_of_proxies = f"""<b>❌Необходимо иметь следующее количество прокси для спам-рассылки: {REDQUIRED_AMOUNT_OF_PROXIES}.
        \nСейчас {amount_of_proxies}/{REDQUIRED_AMOUNT_OF_PROXIES}, добавьте еще с помощью \"➕Добавить прокси\"</b>"""
        return cls._error_insufficient_amount_of_proxies
    
    @classmethod
    @property
    def errorInsufficientAmountOfProxiesForParsing(cls):
        cls.errorInsufficientAmountOfProxiesForParsing = "<b>❌Невозможно спарсить подписчиков из канала без прокси. Добавьте один адрес с помощью \"➕Добавить прокси\"</b>"
        return cls.errorInsufficientAmountOfProxiesForParsing
    
    @classmethod
    def changeStatusAccountInst(cls, status: bool):
        cls._change_status_account_inst = f"<b>Статус аккаунта инстаграм для рассылки сообщений был изменен на: {status}</b>"
        return cls._change_status_account_inst
    
    @classmethod
    @property
    def addProxyText(cls):
        cls.addProxyText = "<b>Введите адрес прокси сервера по образцу: IP_ADDRESS:PORT:LOGIN:PASSWORD</b>"
        return cls.addProxyText
    
    @classmethod
    @property
    def addingProxy(cls):
        cls.addingProxy = "<i>Происходит проверка валидности прокси адреса, ожидайте...</i>"
        return cls.addingProxy

    @classmethod
    @property
    def addedProxyText(cls):
        cls.addedProxyText = "✅<b>Адрес прокси был успешно добавлен в базу данных</b>"
        return cls.addedProxyText
    
    @classmethod
    @property
    def errorProxyAddress(cls):
        cls.errorProxyAddress = "❌<b>Произошла ошибка при добавлении прокси адреса в базу данных</b>"
        return cls.errorProxyAddress
    
    @classmethod
    @property
    def errorProxyAddressRemoval(cls):
        cls.errorProxyAddressRemoval = "❌<b>Произошла ошибка при удалении прокси адреса из базы данных</b>"
        return cls.errorProxyAddressRemoval

    @classmethod
    @property
    def errorInvalidProxyAdress(cls):
        cls.errorInvalidProxyAdress = "❌<b>Введенный прокси адрес не подходит по образцу: IP_ADDRESS:PORT:LOGIN:PASSWORD.\n Перейдите в меню рассылки инстаграма или введите прокси еще раз</b>"
        return cls.errorInvalidProxyAdress
    
    @classmethod
    @property
    def deleteProxyAddress(cls):
        cls.deleteProxyAddress = "<b>Введите адрес прокси сервера для удаления из базы данных по образцу: IP_ADDRESS:PORT:LOGIN:PASSWORD</b>"
        return cls.deleteProxyAddress
    
    @classmethod
    @property
    def deletedProxyAddress(cls):
        cls.deleteProxyAddress = "✅<b>Адрес прокси был успешно удален из базы данных</b>"
        return cls.deleteProxyAddress

    @classmethod
    @property
    def setDelayForInstText(cls):
        cls.setDelayForInstText = "<b>Введите задержку для автоматической рассылки инстаграм в минутах:</b>"
        return cls.setDelayForInstText

    @classmethod
    @property
    def errorNotIntegerInstDelay(cls):
        cls.errorNotIntegerInstDelay = "❌<b>Задержка является натуральным числом, введите её заново или перейдите в меню рассылки инстаграм</b>"
        return cls.errorNotIntegerInstDelay

    @classmethod
    @property
    def delayForInstBeenSetText(cls):
        cls.delayForInstBeenSetText = "<b>✅Новая задержка для автоматической спам рассылки инстаграм была установлена</b>"
        return cls.delayForInstBeenSetText

    @classmethod
    @property
    def updateReelsLinkText(cls):
        cls.updateReelsLinkText = "<b>Введите ссылку для рилза, которая будет использоваться в рассылке:</b>"
        return cls.updateReelsLinkText

    @classmethod
    @property
    def updatedReelsLinkText(cls):
        cls.updatedReelsLinkText = "✅<b>Ссылка на рилз была успешно сохранена в базу данных</b>"
        return cls.updatedReelsLinkText
    
    @classmethod
    @property
    def errorReelsLink(cls):
        cls.updatedReelsLinkText = "❌<b>Произошла ошибка при добавлении ссылки на рилз в базу данных</b>"
        return cls.updatedReelsLinkText

    @classmethod
    @property
    def errorInvalidReelsLink(cls):
        cls.errorInvalidReelsLink = "❌<b>Введенная ссылка не соотвествует ссылке на рилз: паттерн \"https://www\.instagram\.com/reel/[\w\d_-]+/\?utm_source=ig_web_copy_link\"</b>"
        return cls.errorInvalidReelsLink

    @classmethod
    @property
    def errorDelayInst(cls):
        cls.errorDelayInst = "❌<b>Произошла ошибка при добавлении задержки для рассылки инстаграма в базу данных</b>"
        return cls.errorDelayInst


    @classmethod
    @property
    def spamInstText(cls):
        cls.spamInstText = "🔧Настройка аккаунта сессии инстаргам"
        return cls.spamInstText

    @classmethod
    @property
    def sendUpdateMessageText(cls):
        cls.sendUpdateMessageText = "✉️Введите сообщение, которое хотите, чтобы получили другие пользователи:"
        return cls.sendUpdateMessageText

    @classmethod
    @property
    def new_account_state1(cls):
        cls._new_account_state1 = "📩Отправь файл сессии акаунта с уникальным именем в формате: <b>account_name.session</b>"
        return cls._new_account_state1

    @classmethod
    @property
    def spamTgText(cls):
        cls.spamTgText = "🔧Настройка аккаунта сессии телеграм"
        return cls.spamTgText
    
    @classmethod
    async def visualConfigText(cls, account_name, isProfilePicture):
        account = UserAgentCore(account_name)
        entity = await account.getMe()
        first_name = entity.first_name
        last_name = entity.last_name
        username = entity.username
        account_description = await account.getProfileBio(entity)

        if first_name:
            first_name = first_name.replace('_', '\\_')
        if last_name:
            last_name = last_name.replace('_', '\\_')
        if username:
            username = username.replace('_', '\\_')
        if account_description:
            account_description = account_description.replace('_', '\\_')

        visualConfigText = f"""
🌄Визаульная конфигурация аккаунта сессии
first name: {first_name}
second name: {last_name}
username: @{username}
account description: 
--------------------
{account_description}
--------------------
profile picture: {"" if isProfilePicture else "None"}
"""
        # print(visualConfigText)
        def split_string(input_string, max_length=4000):
                result = []
                for i in range(0, len(input_string), max_length):
                    result.append(input_string[i : i + max_length])
                return result
        return split_string(visualConfigText)

    @classmethod
    @property
    def changeProfileDescriptionText(cls):
        cls.storiesMenuText = "<b>Введите сообщение, на которое хотите изменить описание аккаунта сессии:</b>"
        return cls.storiesMenuText

    @classmethod
    @property
    def profileDescriptionChangedText(cls):
        cls.storiesMenuText = "<b>✅Описание аккаунта сессии было успешно обновлено</b>"
        return cls.storiesMenuText

    @classmethod
    @property
    def storiesMenuText(cls):
        cls.storiesMenuText = "👀Настройка просмотра сториз"
        return cls.storiesMenuText

    @classmethod
    @property
    def editAccountsMenuText(cls):
        cls._editAccountsMenuText = "<b>🤖Аккануты:</b>"
        return cls._editAccountsMenuText

    @classmethod
    @property
    def sendChangeAccountMessageText(cls):
        cls._sendChangeAccountMessageText = "💬<b>Укажите рекламное сообщение в MARKDOWN разметке, которое будет базой для перегенерации ChatGPT</b>"
        return cls._sendChangeAccountMessageText

    @classmethod
    @property
    def sendChangePromptText(cls):
        cls._sendChangePromptText = (
            "✍️<b>Укажите подробное описание канала, для prompt ChatGPT</b>"
        )
        return cls._sendChangePromptText

    @classmethod
    @property
    def message_edited(cls):
        cls._message_edited = "<b>✅Текст рекламного сообщения изменено</b>"
        return cls._message_edited

    @classmethod
    @property
    def prompt_edited(cls):
        cls._prompt_edited = "<b>✅Текст prompt изменено</b>"
        return cls._prompt_edited

    @classmethod
    @property
    def target_edited(cls):
        cls._target_edited = "<b>✅Целевой канал изменен</b>"
        return cls._target_edited

    @classmethod
    @property
    def sendChangePromptText(cls):
        cls._sendChangePromptText = "🎯<b>Укажите @username целевого канала.</b>\n<i>Этот @username будет подставляться в рекламное сообщение и prompt для ChatGPT</i>"
        return cls._sendChangePromptText
    
    @classmethod
    @property
    def sendChangeDelayText(cls):
        cls.sendChangeDelayText = "<b>Введите задержку в минутах для рассылки телеграм:</b>"
        return cls.sendChangeDelayText
    
    @classmethod
    @property
    def errorNotIntegerDelayTg(cls):
        cls.errorNotIntegerDelayTg = "<b>❌Задержка является натуральным числом, введите её заново или перейдите в меню спам рассылки телеграм</b>"
        return cls.errorNotIntegerDelayTg

    @classmethod
    @property
    def delayForSpamTgHasBeenSet(cls):
        cls.delayForSpamTgHasBeenSet = "<b>✅Новая задержка для автоматической рассылки телеграм была установлена</b>"
        return cls.delayForSpamTgHasBeenSet

    @classmethod
    @property
    def errorSetTargetChannel(cls):
        cls._errorSetTargetChannel = "❌<b>Ошибка форматирования @username отправьте еще раз или вернитесь в главное меню</b>"
        return cls._errorSetTargetChannel

    @classmethod
    @property
    def sendAddAdvChatText(cls):
        cls._sendAddAdvChatText = (
            "➕<b>Укажите @username чата для рекламы данного канала</b>"
        )
        return cls._sendAddAdvChatText

    @classmethod
    @property
    def adv_chat_added(cls):
        cls._adv_chat_added = "<b>✅Рекламный чат добавлен</b>"
        return cls._adv_chat_added

    @classmethod
    @property
    def adv_chat_removed(cls):
        cls._adv_chat_removed = "✅<b>Рекламный чат удален</b>"
        return cls._adv_chat_removed

    @classmethod
    @property
    def sendRemoveAdvChatText(cls):
        cls._sendRemoveAdvChatText = (
            "➖<b>Укажите @username для удаления чата из рекламного списка чатов</b>"
        )
        return cls._sendRemoveAdvChatText

    @classmethod
    @property
    def ReloadedChatGPTMessageText(cls):
        cls._ReloadedChatGPTMessageText = "✅<b>Рекламное сообщение обновлено</b>"
        return cls._ReloadedChatGPTMessageText

    @classmethod
    @property
    def sendDeleteAccountText(cls):
        cls._sendDeleteAccountText = "🗑<b>Вы точно хотите удалить аккаунт? Напишите: ДА, ТОЧНО - что бы удалить аккаунт</b>"
        return cls._sendDeleteAccountText

    @classmethod
    @property
    def account_deleted(cls):
        cls._account_deleted = "✅<b>Аккаунт и сессия удалены</b>"
        return cls._account_deleted

    @classmethod
    def not_ready_change_status(cls, status: bool):
        cls._change_status = f"❌<b>Не все поля заполнены, аккаунт не готов для использования</b>\nТекущий статус использования аккаунта: <b>{status}</b>"
        return cls._change_status

    @classmethod
    def ready_change_status(cls, status: bool):
        cls._change_status = f"✅<b>Аккаунт готов для использования</b>\nТекущий статус использования аккаунта: <b>{status}</b>"
        return cls._change_status

    @classmethod
    def change_status_menu(cls, session_name: str):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="✅Включить аккаунт",
                        callback_data=f"set_status_on#{session_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="❌Выключить аккаунт",
                        callback_data=f"set_status_off#{session_name}",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data=f"back_to_edit_menu#{session_name}"
                    )
                ],
            ],
        )



    @classmethod
    def back_to_spam_tg(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_spam_tg"
                    )
                ]
            ],
        )
    
    @classmethod
    def back_to_spam_inst(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_spam_inst"
                    )
                ]
            ],
        )
    
    @classmethod
    def back_to_get_password(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_get_password"
                    )
                ]
            ],
        )

    @classmethod 
    def back_to_get_proxy(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_get_proxy"
                    )
                ]
            ],
        )

    @classmethod
    def back_to_edit_inst_account(cls, account_name):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data=f"back_to_edit_inst_account#{account_name}"
                    )
                ]
            ],
        )

    @classmethod
    def back_to_edit_menu(cls, account_name):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data=f"back_to_edit_menu#{account_name}"
                    )
                ]
            ],
        )
    
    @classmethod
    @property
    def back_to_inst_acc_edit(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data=f"back_to_inst_acc_edit"
                    )
                ]
            ],
        )

    @classmethod
    def back_to_vis_cfg_menu(cls, account_name):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data=f"back_to_viscfg_account#{account_name}"
                    )
                ]
            ],
        )

    @classmethod
    def back_to_stories_menu(cls, account_name):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data=f"back_to_look_stories#{account_name}"
                    )
                ]
            ],
        )
    
    @classmethod
    def back_to_aiosheduler_stories(cls, account_name):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data=
                        f"back_to_aiosheduler_stories#{account_name}"
                    )
                ]
            ],
        )

    @classmethod
    def back_to_logging_in_inst(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data=f"back_to_logging_in_inst"
                    )
                ]
            ],
        )
    
    
    @classmethod
    @property
    def addTargetChannelText(cls):
        cls.addTargetChannelText = "<b>Введите название канала для парсинга в виде @username:</b>"
        return cls.addTargetChannelText
    
    @classmethod
    def launchStoriesText(cls, stories_watched):
        cls._launch_stories_text = f"<b>✅Всего было успешно просмотрено следующее количество сториз: {stories_watched}.</b>"
        return cls._launch_stories_text

    @classmethod
    @property
    def errorIncorrectTargetChannel(cls):
        cls.errorIncorrectTargetChannel = "<b>❌Вы ввели неправильный тэг канала (@username), попробуйте еще раз или вернитесь в меню настройки сториз</b>"
        return cls.errorIncorrectTargetChannel
   
    @classmethod
    @property
    def errorDbTargetChannel(cls):
        cls.errorDbTargetChannel = "<b>❌Произошла ошибка при добавлении target channel в базу данных, попробуйте еще раз или вернитесь в меню настройки сториз</b>"
        return cls.errorDbTargetChannel
    
    @classmethod
    @property
    def errorTargetChannelAlreadyExists(cls):
        cls.errorDbTargetChannel = "<b>❌Данный target сhannel уже существует в базе данных, попробуйте еще раз или вернитесь в меню настройки сториз</b>"
        return cls.errorDbTargetChannel
    
    @classmethod
    @property
    def errorNonExistentChannelUsername(cls):
        cls.errorNonExistentChannelUsername = "<b>❌Вы ввели username канала, который не существует, попробуйте еще раз или вернитесь в меню настройки сториз</b>"
        return cls.errorNonExistentChannelUsername
    
    @classmethod
    @property
    def errorNoAdminPrivileges(cls):
        cls.errorNoAdminPrivileges = "<b>❌Вы ввели username канала, к которому у вас нет прав администратора, попробуйте еще раз или вернитесь в меню настройки сториз</b>"
        return cls.errorNoAdminPrivileges

    @classmethod
    @property
    def addedTargetChannelText(cls):
        cls.errorIncorrectTargetChannel = "<b>✅Таргетный канал для прасинга был успешно добавлен в базу данных</b>"
        return cls.errorIncorrectTargetChannel

    @classmethod
    @property
    def deleteTargetChannelText(cls):
        cls.deleteTargetChannelText = "<b>Введите название канала для парсинга, который вы хотите удалить, в виде @username:</b>"
        return cls.deleteTargetChannelText


    @classmethod
    @property
    def errorDbNonExistentTargetChannel(cls):
        cls.deleteTargetChannelText = "<b>❌Вы пытаетесь удалить канал, который не существует в базе данных, попробуйте еще раз или вернитесь в меню настройки сториз</b>"
        return cls.deleteTargetChannelText

    @classmethod
    @property
    def deletedTargetChannelText(cls):
        cls.deletedTargetChannelText = "<b>✅Таргетный канал для прасинга был успешно удален из базы данных</b>"
        return cls.deletedTargetChannelText

    @classmethod
    @property
    def setDelayForAioschedulerText(cls):
        cls.setDelayForAioscheduler = "<b>Введите задержку для автоматического просмотра сториз в минутах:</b>"
        return cls.setDelayForAioscheduler
    
    @classmethod
    @property
    def errorNotIntegerDelay(cls):
        cls.errorNotIntegerDelay = "<b>❌Задержка является натуральным числом, введите её заново или перейдите в меню отслеживания сториз</b>"
        return cls.errorNotIntegerDelay

    @classmethod
    @property
    def delayForAioschedulerBeenSetText(cls):
        cls.setDelayForAioscheduler = "<b>✅Новая задержка для автоматического просмотра сториз была установлена</b>"
        return cls.setDelayForAioscheduler
    
    @classmethod
    def changeStatusForAioschedulerText(cls, status: bool):
        cls._change_aiosheduler_status = f"<b>Статус аккаунта для отслеживания сториз был изменен на: {status}</b>"
        return cls._change_aiosheduler_status
    
    @classmethod
    @property
    def errorAioscheduleStoriesActive(cls):
        cls.errorAioscheduleStoriesActive = "<b>❌В настоящее время включено отслеживание сториз.\n Поменяйте статус аккаунта в \"👀Отслеживание сториз\"</b>"
        return cls.errorAioscheduleStoriesActive
    
    @classmethod
    @property
    def errorNoTargetChannels(cls):
        cls.errorNoTargetChannels = "<b>❌Нет таргетных каналов, из которых можно спарсить подписчиков.\n Добавьте их с помощью \"➕Добавить аккаунт для парсинга премиум пользователей\"</b>"
        return cls.errorNoTargetChannels

    @classmethod
    @property
    def editFirstNameText(cls):
        cls.editFirstNameText = "<b>Введите текст, на который ты хочешь поменять first_name этого аккаунта сессии:</b>"
        return cls.editFirstNameText

    @classmethod
    @property
    def editLastNameText(cls):
        cls.editLastNameText = "<b>Введите текст, на который ты хочешь поменять last_name этого аккаунта сессии:</b>"
        return cls.editLastNameText
    
    @classmethod
    @property
    def editUsernameText(cls):
        cls.editUsernameText = "<b>Введите текст, на который ты хочешь поменять username этого аккаунта сессии:</b>"
        return cls.editUsernameText
    
    @classmethod
    @property
    def profilePictureChangedText(cls):
        cls.profilePictureChangedText = "<b>✅ Аватарка профиля был успешно изменена</b>"
        return cls.profilePictureChangedText

    @classmethod
    @property
    def usernameChangedText(cls):
        cls.usernameChangedText = "<b>✅ Username был успешно изменен</b>"
        return cls.usernameChangedText

    @classmethod
    @property
    def errorUsernameTaken(cls):
        cls.errorEditUsername = "<b>❌ Username, который вы ввели, уже занят другим пользователем. Введите его еще раз или вернитесь в меню редактирования визуального конфига</b>"
        return cls.errorEditUsername
    
    @classmethod
    def errorUsernameFloodWait(cls, time_left):
        cls._error_username_floodWait = f"<b>❌ Вы изменяли свой username слишком часто за последнее время. До следующего изменения username осталось {time_left} секунд</b>"
        return cls._error_username_floodWait

    @classmethod
    @property
    def errorSameUsername(cls):
        cls.errorEditUsername = "<b>❌ Username, который вы ввели, не отличается от текущего. Введите его еще раз или вернитесь в меню редактирования визуального конфига</b>"
        return cls.errorEditUsername
    
    @classmethod
    @property
    def changeProfilePictureText(cls):
        cls.changeProfilePictureText = "<b>Загрузи фотографию в формате .jpg, .jpeg или .png, на которую хочешь изменить фотографию аккаунта:</b>"
        return cls.changeProfilePictureText
    
    @classmethod
    @property
    def errorProfilePicture(cls):
        cls.changeProfilePictureText = "<b>❌ Неверное расширение файла для аватарки профиля. Загрузите файл еще раз или вернитесь в меню редактирования визуального конфига</b>"
        return cls.changeProfilePictureText


