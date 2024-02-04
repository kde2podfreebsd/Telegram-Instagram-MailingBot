from App.Bot.Markups import MarkupBuilder

from App.Config import bot
from App.Config import message_context_manager
from App.Config import account_context

from App.Logger import ApplicationLogger

from App.Database.DAL.AccountStoriesDAL import AccountStoriesDAL
from App.Database.session import async_session

from App.UserAgent.UserAgentDbPremiumUsers import DbPremiumUsersExceptions
from App.UserAgent.Core import UserAgentCore

from telebot.asyncio_handler_backends import State, StatesGroup

import re
import aioschedule

logger = ApplicationLogger()

class StoriesMenuStates(StatesGroup):
    AddTargetChat = State()
    DeleteTargetChat = State()
    SetDelay = State()
    ChangeStatus = State()

async def _sendAddTargetChatText(message):

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.addTargetChannelText,
        reply_markup=MarkupBuilder.back_to_stories_menu(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

    await bot.set_state(message.chat.id, StoriesMenuStates.AddTargetChat)

async def _errorTargetChat(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorIncorrectTargetChannel,
        reply_markup=MarkupBuilder.back_to_stories_menu(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, state=StoriesMenuStates.AddTargetChat)

async def _errorDbTargetChat(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorDbTargetChannel,
        reply_markup=MarkupBuilder.back_to_stories_menu(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, state=StoriesMenuStates.AddTargetChat)

async def _errorNonExistentChannelUsername(message):
    
    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorNonExistentChannelUsername,
        reply_markup=MarkupBuilder.back_to_stories_menu(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, state=StoriesMenuStates.AddTargetChat)

async def _errorNoAdminPrivileges(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorNoAdminPrivileges,
        reply_markup=MarkupBuilder.back_to_stories_menu(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, state=StoriesMenuStates.AddTargetChat)

@bot.message_handler(state=StoriesMenuStates.AddTargetChat)
async def _addTargetChat(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )
    channel_username = message.text
    db_exceptions = DbPremiumUsersExceptions(
        username=channel_username[1:]
    )

    pattern = r"^@[A-Za-z0-9]+(_[A-Za-z0-9]+)*$"
    if (re.match(pattern, channel_username)):
        async with async_session() as session:
            account_stories_dal = AccountStoriesDAL(session)
            result = await account_stories_dal.addTargetChannel(
                username=channel_username,
                session_name=account_context.account_name[message.chat.id]
            )

            if (db_exceptions.WRONG_USERNAME_EXCEPTION == result):
                await _errorNonExistentChannelUsername(message)

            elif (db_exceptions.ADMIN_PRIVILEGES_EXCEPTION == result):
                await _errorNoAdminPrivileges(message)

            else:
                if (result):
                    msg = await bot.send_message(
                        message.chat.id,
                        MarkupBuilder.addedTargetChannelText,
                        reply_markup=MarkupBuilder.back_to_stories_menu(
                            account_name = account_context.account_name[message.chat.id]
                        ),
                        parse_mode="HTML"
                    )
                    await message_context_manager.add_msgId_to_help_menu_dict(
                        chat_id=message.chat.id, 
                        msgId=msg.message_id
                    )
                else:
                    await _errorDbTargetChat(message)
    else:
        await _errorTargetChat(message)


async def _sendDeleteTargetChatText(message):
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.deleteTargetChannelText,
        reply_markup=MarkupBuilder.back_to_stories_menu(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

    await bot.set_state(message.chat.id, StoriesMenuStates.DeleteTargetChat)

async def _errorDbNonExistentTargetChannel(message):
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorDbNonExistentTargetChannel,
        reply_markup=MarkupBuilder.back_to_stories_menu(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

    await bot.set_state(message.chat.id, StoriesMenuStates.DeleteTargetChat)

@bot.message_handler(state=StoriesMenuStates.DeleteTargetChat)
async def _deleteTargetChat(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )
    channel_username = message.text
    pattern = r"^@[A-Za-z0-9]+(_[A-Za-z0-9]+)*$"
    if (re.match(pattern, channel_username)):
        async with async_session() as session:
            account_stories_dal = AccountStoriesDAL(session)
            result = await account_stories_dal.removeTargetChannel(
                session_name=account_context.account_name[message.chat.id]
            )
            if (result):
                msg = await bot.send_message(
                    message.chat.id,
                    MarkupBuilder.deletedTargetChannelText,
                    reply_markup=MarkupBuilder.back_to_stories_menu(
                        account_name = account_context.account_name[message.chat.id]
                    ),
                    parse_mode="HTML"
                )
                await message_context_manager.add_msgId_to_help_menu_dict(
                    chat_id=message.chat.id, 
                    msgId=msg.message_id
                )
            else:
                await _errorDbNonExistentTargetChannel(message)

    else:
        await _errorTargetChat(message)

async def _launchStories(message):
    async with async_session() as session:
        account_stories_dal = AccountStoriesDAL(session)
        result = await account_stories_dal.getAccountBySessionName(
            session_name=account_context.account_name[message.chat.id]
        )
        usernames = await account_stories_dal.getPremiumMemebers(
            account_stories_id=result.id
        )
        userAgent = UserAgentCore(
            session_name=account_context.account_name[message.chat.id]
        )
        stories_watched = await userAgent.giveReaction(usernames)
        msg = await bot.send_message(
            message.chat.id,
            MarkupBuilder.launchStoriesText(stories_watched),
            reply_markup=MarkupBuilder.back_to_stories_menu(
                account_name = account_context.account_name[message.chat.id]
            ),
            parse_mode="HTML"
        )
        await message_context_manager.add_msgId_to_help_menu_dict(
            chat_id=message.chat.id, 
            msgId=msg.message_id
    )

async def _setDelayForAioschedulerText(message):
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.setDelayForAioschedulerText,
        reply_markup=MarkupBuilder.back_to_aiosheduler_stories_service(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

    await bot.set_state(message.chat.id, StoriesMenuStates.SetDelay)

@bot.message_handler(state=StoriesMenuStates.SetDelay)
async def _setDelayForAioscheduler(message):
    async with async_session() as session:
        account_stories_dal = AccountStoriesDAL(session)
        account = await account_stories_dal.getAccountBySessionName(
            session_name=account_context.account_name[message.chat.id]
        )
        print(account.delay)
        account.delay = int(message.text)

    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.DelayForAioschedulerBeenSetText,
        reply_markup=MarkupBuilder.back_to_aiosheduler_stories_service(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

