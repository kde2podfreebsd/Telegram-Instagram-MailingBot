from telebot import formatting
from telebot import types
from telebot.types import ReplyKeyboardMarkup


class MarkupBuilder(object):

    _new_account_state1 = None
    _hide_menu: object = None
    _welcome_text: object = None

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
