import asyncio
import os

from telebot import formatting
from telebot import types
from telebot.types import ReplyKeyboardMarkup

from App.Database.DAL.AccountDAL import AccountDAL
from App.Database.session import async_session


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
                        text="🔙Назад", callback_data=f"back_to_editAccounts_menu"
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
    def main_menu(cls):
        menu: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(
            row_width=1,
            resize_keyboard=True,
            one_time_keyboard=True,
        ).add(
            types.KeyboardButton("🤖 Добавить аккаунт"),
            types.KeyboardButton("🛠 Редактировать аккаунты"),
            types.KeyboardButton("📝 Логи"),
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
        cls._new_account_state1 = "📩Отправь файл сессии акаунта с уникальным именем в формате: <b>account_name.session</b>"
        return cls._new_account_state1

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
