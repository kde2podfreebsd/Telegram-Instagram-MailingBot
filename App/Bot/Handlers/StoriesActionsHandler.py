from App.Bot.Markups import MarkupBuilder

from App.Config import bot
from App.Config import message_context_manager

from App.Logger import ApplicationLogger

from App.Database.DAL.TargetChannelDAL import TargetChannelDAL
from App.Database.session import async_session

from App.UserAgent.UserAgentDbPremiumUsers import DbPremiumUsersExceptions
from App.UserAgent.Core import UserAgentCore

from telebot.asyncio_handler_backends import State, StatesGroup

import re
import os

logger = ApplicationLogger()

class StoriesMenuStates(StatesGroup):
    AddTargetChat = State()
    DeleteTargetChat = State()

async def _sendAddTargetChatText(message):

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.addTargetChannelText,
        reply_markup=MarkupBuilder.back_to_stories_menu(),
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
        reply_markup=MarkupBuilder.back_to_stories_menu(),
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
        reply_markup=MarkupBuilder.back_to_stories_menu(),
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
        reply_markup=MarkupBuilder.back_to_stories_menu(),
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
        reply_markup=MarkupBuilder.back_to_stories_menu(),
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
            target_channel_dal = TargetChannelDAL(session)
            result = await target_channel_dal.create_target_channel(
                username=channel_username,
                session_name=os.getenv("SESSION_NAME_FOR_TG_ACCESS")
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
                        reply_markup=MarkupBuilder.back_to_stories_menu(),
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
        reply_markup=MarkupBuilder.back_to_stories_menu(),
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
        reply_markup=MarkupBuilder.back_to_stories_menu(),
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
            target_channel_dal = TargetChannelDAL(session)
            result = await target_channel_dal.delete_target_channel(
                username=channel_username
            )
            if (result):
                msg = await bot.send_message(
                    message.chat.id,
                    MarkupBuilder.deletedTargetChannelText,
                    reply_markup=MarkupBuilder.back_to_stories_menu(),
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
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.launchStoriesText,
        reply_markup=MarkupBuilder.back_to_stories_menu(),
        parse_mode="HTML"
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    async with async_session() as session:
        target_channel_dal = TargetChannelDAL(session)
        usernames = await target_channel_dal.get_premium_members()
        print(usernames)
        userAgent = UserAgentCore(
            session_name=os.getenv("SESSION_NAME_FOR_TG_ACCESS")
        )
        await userAgent.giveReaction(usernames)

