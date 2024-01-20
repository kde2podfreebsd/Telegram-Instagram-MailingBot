import telebot
from telethon import TelegramClient
import telethon.tl.functions

from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup

from App.Config import bot
from App.Bot.Markups import MarkupBuilder
from App.Config import message_context_manager
from App.Config import sessions_dirPath
from App.Config import account_context
from App.Logger import ApplicationLogger
import os 

from App.Bot.Handlers.EditAccountVisualMenuHandler import _visualConfig



class EditAccountVisCfgActionStates(StatesGroup):
    EditFirstName = State()
    EditLastName = State()
    EditUsername = State()
    EditPhoto = State()


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
    chat_id = message.chat.id
    account_name = account_context.account_name[chat_id]
    session_path = f"{sessions_dirPath}/{account_name}"
    
    new_first_name = message.text
    async with TelegramClient(session_path, api_id=123, api_hash="123") as client:

        await client(telethon.tl.functions.account.UpdateProfileRequest(
            first_name=new_first_name
        ))
    await _visualConfig(account_name=account_context.account_name[chat_id], message=message)

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
    account_name = account_context.account_name[chat_id]
    session_path = f"{sessions_dirPath}/{account_name}"
    
    new_last_name = message.text
    async with TelegramClient(session_path, api_id=123, api_hash="123") as client:
 
        await client(telethon.tl.functions.account.UpdateProfileRequest(
            last_name=new_last_name
        ))
    await _visualConfig(account_name=account_context.account_name[chat_id], message=message)

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
    
@bot.message_handler(state=EditAccountVisCfgActionStates.EditUsername)
async def edit_username(message):
    chat_id=message.chat.id
    account_name = account_context.account_name[chat_id]
    session_path = f"{sessions_dirPath}/{account_name}"
    
    new_username= message.text
    async with TelegramClient(session_path, api_id=123, api_hash="123") as client:

        await client(telethon.tl.functions.account.UpdateUsernameRequest(new_username))
    await _visualConfig(account_name=account_context.account_name[chat_id], message=message)

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


# state=EditAccountVisCfgActionStates.EditPhoto
@bot.message_handler(content_types=["photo"])
async def edit_pfp(message):
    chat_id=message.chat.id
    account_name = account_context.account_name[chat_id]
    session_path = f"{sessions_dirPath}/{account_name}"    
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_content = await bot.download_file(file_info.file_path)

    with open("temp_photo.jpg", "wb") as temp_file:
        temp_file.write(file_content)

    # Загрузка временного файла в Telegram
    async with TelegramClient('session_name', 
        api_id = 123, 
        api_hash = '123'
    ) as client:
        file_result = await client.upload_file("temp_photo.jpg")
        await client(telethon.tl.functions.photos.UploadProfilePhotoRequest(file=file_result))

    await _visualConfig(account_name=account_context.account_name[chat_id], message=message)

    os.remove("temp_photo.jpg")
    
