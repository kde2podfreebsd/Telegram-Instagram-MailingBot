import asyncio

from telebot.asyncio_filters import ForwardFilter
from telebot.asyncio_filters import IsDigitFilter
from telebot.asyncio_filters import IsReplyFilter
from telebot.asyncio_filters import StateFilter

from App.Bot.Handlers.LogsHandler import _sendLog
from App.Bot.Handlers.MainMenuHandler import _mainMenu
from App.Bot.Handlers.MainMenuHandler import send_welcome  # noqa
from App.Bot.Handlers.NewAccountHandler import _newAccountMenu
from App.Bot.Markups import MarkupBuilder  # noqa
from App.Bot.Middlewares import FloodingMiddleware
from App.Config import bot
from App.Config import message_context_manager
from App.Config import singleton


@singleton
class Bot:
    def __init__(self):
        bot.add_custom_filter(IsReplyFilter())
        bot.add_custom_filter(ForwardFilter())
        bot.add_custom_filter(StateFilter(bot))
        bot.add_custom_filter(IsDigitFilter())
        bot.setup_middleware(FloodingMiddleware(1))

    @staticmethod
    @bot.message_handler(content_types=["text"])
    async def HandlerTextMiddleware(message):
        if message.text == "📝 Логи":
            await _sendLog(message)

        if message.text == "🔙Назад":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=message.chat.id
            )
            await _mainMenu(message=message)

        if message.text == "🤖 Добавить аккаунт":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=message.chat.id
            )
            await _newAccountMenu(message)

    @staticmethod
    @bot.callback_query_handler(func=lambda call: True)
    async def HandlerInlineMiddleware(call):
        if call.data == "back_to_main_menu":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _mainMenu(message=call.message)

    @staticmethod
    async def polling():
        task1 = asyncio.create_task(bot.infinity_polling())
        await task1


if __name__ == "__main__":
    b = Bot()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(b.polling())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
