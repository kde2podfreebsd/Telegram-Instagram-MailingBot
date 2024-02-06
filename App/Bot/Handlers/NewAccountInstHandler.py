from App.Bot.Markups import MarkupBuilder
from App.Config import bot
from App.Config import message_context_manager
from App.Config import login_context
from App.Config import inst_sessions_dirPath
import asyncio

from App.Parser.InstagramParser import InstagramParser
from App.Parser.InstagramParser import InstagramParserExceptions

from App.Database.DAL.AccountInstDAL import AccountInstDAL
from App.Database.session import async_session

from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup



class NewAccountInstStates(StatesGroup):
    LoggingIn = State()
    GetPassword = State()

async def _getInstAccountLogin(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.getInstAccountLogin,
        reply_markup=MarkupBuilder.back_to_spam_inst(),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, NewAccountInstStates.GetPassword)

@bot.message_handler(state=NewAccountInstStates.GetPassword)
async def _getInstAccountPassword(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )

    login_context.updateLogin(
        chat_id=chat_id, 
        login=message.text
    )
    
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.getInstAccountPassword,
        reply_markup=MarkupBuilder.back_to_logging_in_inst(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, NewAccountInstStates.LoggingIn)

async def _errorLogginIn(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    msg = await bot.send_message(
        message.chat.id,
        text=MarkupBuilder.errorInstLoggingIn,
        reply_markup=MarkupBuilder.back_to_spam_inst(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.delete_state(message.chat.id, message.chat.id)

async def _errorIncorrectPasswordOrLogin(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    msg = await bot.send_message(
        message.chat.id,
        text=MarkupBuilder.errorIncorrectPasswordOrLogin,
        reply_markup=MarkupBuilder.back_to_spam_inst(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.delete_state(message.chat.id, message.chat.id)

async def _errorSuspendedAccount(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    msg = await bot.send_message(
        message.chat.id,
        text=MarkupBuilder.errorSuspendedAccount,
        reply_markup=MarkupBuilder.back_to_spam_inst(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.delete_state(message.chat.id, message.chat.id)

@bot.message_handler(state=NewAccountInstStates.LoggingIn)
async def _newAccountLoggingIn(message):
    instagramParserExceptions = InstagramParserExceptions()
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )

    login = login_context.login[chat_id]
    password = message.text
    instagramParser = InstagramParser(
        login=login,
        password=password
    )

    exception = await instagramParser.async_logging_in()
    if exception == None:
        msg = await bot.send_message(
            message.chat.id,
            text=MarkupBuilder.instLoggingInSuccessfullyText,
            reply_markup=MarkupBuilder.back_to_spam_inst(),
            parse_mode="HTML",
        )
        async with async_session() as session:
            account_inst_dal = AccountInstDAL(session)
            session_name = login
            await account_inst_dal.createAcount(session_name=session_name)

        await message_context_manager.add_msgId_to_help_menu_dict(
            chat_id=message.chat.id, msgId=msg.message_id
        )
    elif str(exception) == str(instagramParserExceptions.IncorrectPasswordOrLogin):
        await _errorIncorrectPasswordOrLogin(message)
    elif str(exception) == str(instagramParserExceptions.SuspendedAccount):
        await _errorSuspendedAccount(message)
    else:
        await _errorLogginIn(message)
