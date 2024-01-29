from App.Bot.Markups import MarkupBuilder
from App.Config import bot
from App.Config import message_context_manager
import asyncio

from App.Parser.InstagramParser import InstagramParser

from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup



class NewAccountInstStates(StatesGroup):
    LoggingInManually = State()

async def _newAccountLoggingIn(message):
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.instLoggingInText,
        reply_markup=MarkupBuilder.AccountInstLoggingInMenu(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

async def _newAccountLoggingInCookies(message):

    msg_to_del = await bot.send_message(
        message.chat.id,
        "⚙️",
        reply_markup=MarkupBuilder.hide_menu,
        parse_mode="MarkdownV2",
    )

    await bot.delete_message(
        chat_id=message.chat.id, message_id=msg_to_del.message_id, timeout=0
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.new_account_state1,
        reply_markup=MarkupBuilder.back_to_new_inst_account_menu(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

async def _newAccountLoggingInManuallyText(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.instLoginAndPasswordQueryText,
        reply_markup=MarkupBuilder.back_to_new_inst_account_menu(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, NewAccountInstStates.LoggingInManually)

@bot.message_handler(state=NewAccountInstStates.LoggingInManually)
async def _newAccountLoggingInManually(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    login, password = message.text.split(" ")
    instagramParser = InstagramParser(
        login=login,
        password=password
    )


    exception = await instagramParser.logging_in()
    print(exception, type(exception))
    if exception is None:
        msg = await bot.send_message(
            message.chat.id,
            text=MarkupBuilder.instLoggingInSuccessfullyText,
            reply_markup=MarkupBuilder.back_to_spam_inst(),
            parse_mode="HTML",
        )

        await message_context_manager.add_msgId_to_help_menu_dict(
            chat_id=message.chat.id, msgId=msg.message_id
        )
    else:
        msg = await bot.send_message(
            message.chat.id,
            text=MarkupBuilder.errorInstLoggingIn,
            reply_markup=MarkupBuilder.back_to_new_inst_account_menu(),
            parse_mode="HTML",
        )

        await message_context_manager.add_msgId_to_help_menu_dict(
            chat_id=message.chat.id, msgId=msg.message_id
        )
        await bot.set_state(message.chat.id, state=NewAccountInstStates.LoggingInManually)

