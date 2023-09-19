import asyncio
import os

from telebot import formatting
from telebot import types
from telebot.types import ReplyKeyboardMarkup

from App.Database.DAL.AccountDAL import AccountDAL
from App.Database.session import async_session


class MarkupBuilder(object):

    _editAccountsMenuText: object = None
    _new_account_state1: object = None
    _hide_menu: object = None
    _welcome_text: object = None

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
                    text="🔙Назад", callback_data="back_to_main_menu"
                )
            )

            return mp

    @classmethod
    def AccountEditActions(cls, account_name):
        return types.InlineKeyboardMarkup(
            row_width=2,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="💬Изменить сообщение",
                        callback_data="change_acc_msg#account_name",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="➕Добавить рекламный чат",
                        callback_data="add_adv_chat#account_name",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="➖Убрать рекламный чат",
                        callback_data="remove_adv_chat#account_name",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🎯Изменить целевой канал",
                        callback_data="change_target_channel#account_name",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🆙Изменить статус",
                        callback_data="change_status#account_name",
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_editAccounts_menu"
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
                    advertising_channels += f"{x}\n"
            else:
                advertising_channels = "Нет чатов для рекламы"

            out_message = f"""🤖Аккаунт: {os.path.splitext(os.path.basename(account.session_file_path))[0]}
🎯Целевой канал: {account.target_chat}
🆙Статус: {"Актвиен" if account.status else "Не активен"}
💬Рекламное сообщение: {account.message}
📝Чаты для рекламы: {advertising_channels}
"""

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
    def main_menu(cls):
        menu: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
            row_width=1,
            resize_keyboard=True,
            one_time_keyboard=True,
        ).add(
            types.KeyboardButton("🤖 Добавить аккаунт"),
            types.KeyboardButton("🛠 Редактировать аккаунты"),
            types.KeyboardButton("📝 Логи"),
            types.KeyboardButton("💬 ChatGPT"),
        )
        return menu

    @classmethod
    @property
    def welcome_text(cls):
        cls._welcome_text: object = formatting.format_text(
            formatting.mbold(
                "👋Приветствую! Это бот для управления автоматизированной рассылкой в телеграмм."
            ),
            "🔢Выбери необходимый пункт меню",
            separator="\n",
        )
        return cls._welcome_text

    @classmethod
    @property
    def new_account_state1(cls):
        cls._new_account_state1 = "Отправь файл сессии акаунта с уникальным именем в формате: <b>account_name.session</b>"
        return cls._new_account_state1

    @classmethod
    @property
    def editAccountsMenuText(cls):
        cls._editAccountsMenuText = "<b>🤖Аккануты:</b>"
        return cls._editAccountsMenuText

    @classmethod
    def back_to_menu(cls):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="back_to_main_menu"
                    )
                ]
            ],
        )
