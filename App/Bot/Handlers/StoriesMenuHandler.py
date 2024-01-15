import telebot

from App.Bot.Markups import MarkupBuilder
from App.Config import bot
from App.Config import message_context_manager
from App.Config import sessions_dirPath
from App.Database.DAL.AccountDAL import AccountDAL
from App.Database.session import async_session

async def _stories(message, account_name):
    msg = await bot.send_message(message.chat.id, 
        MarkupBuilder.serviceMenuText,
        reply_markup=MarkupBuilder.StoriesMenu(account_name=account_name),
        parse_mode="MarkdownV2"
    )
    
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

async def _accountSessionsListStories(message):
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
        MarkupBuilder.editAccountsMenuText,
        reply_markup=await MarkupBuilder.AccountListKeyboardStroies(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

