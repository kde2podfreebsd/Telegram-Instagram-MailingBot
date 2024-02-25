import telebot
from telethon import TelegramClient
import telethon.tl.functions

from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup

from App.Config import bot
from App.Bot.Markups import MarkupBuilder
from App.Config import message_context_manager
from App.Config import account_context
from App.UserAgent.Core import UserAgentCore
from App.Logger import ApplicationLogger

import re

from App.Bot.Handlers.EditAccountVisualMenuHandler import _visualConfig

logger = ApplicationLogger()

class EditAccountVisCfgActionStates(StatesGroup):
    EditFirstName = State()
    EditLastName = State()
    EditUsername = State()
    EditPhoto = State()
    EditAccountDescription = State()


async def _sendChangeFirstNameText(message):
    chat_id = message.chat.id
    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.editFirstNameText,
        reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountVisCfgActionStates.EditFirstName)
    
@bot.message_handler(state=EditAccountVisCfgActionStates.EditFirstName)
async def edit_first_name(message):
    chat_id=message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    account_name = account_context.account_name[chat_id]
    account = UserAgentCore(account_name)
    await account.editFirstName(new_first_name=message.text)
    
    await _visualConfig(account_name=account_name, message=message)

async def _sendChangeLastNameText(message):
    chat_id = message.chat.id
    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.editLastNameText,
        reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountVisCfgActionStates.EditLastName)
    
@bot.message_handler(state=EditAccountVisCfgActionStates.EditLastName)
async def edit_last_name(message):
    chat_id=message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    account_name = account_context.account_name[chat_id]
    account = UserAgentCore(account_name)
    await account.editLastName(new_last_name=message.text)

    await _visualConfig(account_name=account_name, message=message)

async def _sendChangeUsernameText(message):
    chat_id = message.chat.id
    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.editUsernameText,
        reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountVisCfgActionStates.EditUsername)

async def _errorUsernameTaken(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorSameUsername,
        reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountVisCfgActionStates.EditUsername)

async def _errorSameUsername(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorUsernameTaken,
        reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountVisCfgActionStates.EditUsername)

async def _errorFloodWaitLimitation(message, time_left):
    chat_id = message.chat.id
    account_name = account_context.account_name[chat_id]
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorUsernameFloodWait(time_left=time_left),
        reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

@bot.message_handler(state=EditAccountVisCfgActionStates.EditUsername)
@logger.exception_handler
async def edit_username(message):
    chat_id=message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    account_name = account_context.account_name[chat_id]
    account = UserAgentCore(account_name)
    new_username = message.text
    try:
        await account.editUsername(new_username=new_username)
    except Exception as e:
        error_message = str(e)
        username_taken_exception = re.search(
            r'The username is already taken \(caused by UpdateUsernameRequest\)',
            error_message
        )
        same_username_exception = re.search(
            r'The username is not different from the current username \(caused by UpdateUsernameRequest\)', 
            error_message
        )
        floodwait_limitation = re.search(
            r'A wait of', 
            error_message
        )
        if same_username_exception:
            logger.log_warning(f"The same username {new_username} has been inputted")
            await _errorUsernameTaken(message)
        elif username_taken_exception:
            logger.log_error(f"Username {new_username} has already been occupied")
            await _errorSameUsername(message)
        elif floodwait_limitation:
            logger.log_error(f"Username has been changed a lot recently (Telegram floodwait limitation)")
            time_left = digits = re.findall(r'\d+', error_message)
            await _errorFloodWaitLimitation(message, time_left[0])
    else:
        msg = await bot.send_message(
            message.chat.id,
            MarkupBuilder.usernameChangedText,
            reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
            parse_mode="HTML"
        )

        await message_context_manager.add_msgId_to_help_menu_dict(
            chat_id=message.chat.id, 
            msgId=msg.message_id
        )
            

async def _sendChangeProfilePictureText(message):
    chat_id = message.chat.id
    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.changeProfilePictureText,
        reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
        parse_mode="HTML"
    )
    
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountVisCfgActionStates.EditPhoto)

async def _errorProfilePicture(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorProfilePicture,
        reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

@bot.message_handler(content_types=["photo"])
async def edit_pfp(message):
    chat_id=message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    account_name = account_context.account_name[chat_id] 
    photo = message.photo[-1]
    
    file_info = await bot.get_file(photo.file_id)
    file_content = await bot.download_file(file_info.file_path)

    account = UserAgentCore(account_name)  
    await account.changeProfilePicture(file_content)

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.profilePictureChangedText,
        reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    
async def _sendChangeAccountDescriptionText(message):
    chat_id = message.chat.id

    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.changeProfileDescriptionText,
        reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountVisCfgActionStates.EditAccountDescription)

@bot.message_handler(state=EditAccountVisCfgActionStates.EditAccountDescription)
async def edit_account_description(message):
    chat_id=message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    account_name = account_context.account_name[chat_id] 
    new_account_description = message.text
    
    account = UserAgentCore(account_name)  
    await account.changeProfileDescription(new_account_description)

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.profileDescriptionChangedText,
        reply_markup=MarkupBuilder.back_to_vis_cfg_menu(account_name=account_name),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

    
    
