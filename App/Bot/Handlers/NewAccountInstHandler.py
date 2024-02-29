from App.Bot.Markups import MarkupBuilder
from App.Config import bot
from App.Config import message_context_manager
from App.Config import login_password_context
from App.Config import inst_sessions_dirPath
import re

from App.Parser.InstagramParser import InstagramParser
from App.Parser.InstagramParser import InstagramParserExceptions

from App.Database.DAL.AccountInstDAL import AccountInstDAL
from App.Database.session import async_session

from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup



class NewAccountInstStates(StatesGroup):
    LoggingIn = State()
    GetPassword = State()
    GetProxy = State()

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
    await bot.delete_state(message.chat.id, message.chat.id)
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    if (message.text != "Введите адрес прокси сервера по образцу: IP_ADDRESS:PORT:LOGIN:PASSWORD"):
        login_password_context.updateLogin(
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
    await bot.set_state(message.chat.id, NewAccountInstStates.GetProxy)

async def _errorGetProxyAddress(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    msg = await bot.send_message(
        message.chat.id,
        text=MarkupBuilder.errorGetProxyAddress,
        reply_markup=MarkupBuilder.back_to_spam_inst(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, NewAccountInstStates.LoggingIn)

@bot.message_handler(state=NewAccountInstStates.GetProxy)
async def _getProxyAddress(message):
    await bot.delete_state(message.chat.id, message.chat.id)
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )

    login_password_context.updatePassword(
        chat_id=chat_id, 
        password=message.text
    )
    
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.getProxyAddress,
        reply_markup=MarkupBuilder.back_to_get_password(),
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

async def _errorExpiredProxy(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    msg = await bot.send_message(
        message.chat.id,
        text=MarkupBuilder.errorExpiredProxy,
        reply_markup=MarkupBuilder.back_to_spam_inst(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

async def _errorCaptchaVerification(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    msg = await bot.send_message(
        message.chat.id,
        text=MarkupBuilder.errorCaptchaVerification,
        reply_markup=MarkupBuilder.back_to_spam_inst(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

@bot.message_handler(state=NewAccountInstStates.LoggingIn)
async def _newAccountLoggingIn(message):
    await bot.delete_state(message.chat.id, message.chat.id)
    instagramParserExceptions = InstagramParserExceptions()
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    proxy = message.text
    proxy_pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+:[A-Za-z0-9]+:[A-Za-z0-9]+)$'
    if (re.match(proxy_pattern, proxy)):
        login = login_password_context.login[chat_id]
        password = login_password_context.password[chat_id]
        instagramParser = InstagramParser(
            login=login,
            password=password,
            proxy=proxy
        )

        msg_filler = await bot.send_message(
            message.chat.id,
            MarkupBuilder.loggingIn,
            parse_mode="HTML"
        )

        exception = await instagramParser.async_logging_in()
        if (str(instagramParserExceptions.ProxyConnectionFailed) not in str(exception)):
            await bot.delete_message(
                chat_id=message.chat.id, 
                message_id=msg_filler.id
            )
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
            elif str(exception) == str(instagramParserExceptions.CaptchaVerification):
                await _errorCaptchaVerification(message)
            else:
                await _errorLogginIn(message)
        else:
            await _errorExpiredProxy(message)

    else:
        await _errorGetProxyAddress(message)

    
