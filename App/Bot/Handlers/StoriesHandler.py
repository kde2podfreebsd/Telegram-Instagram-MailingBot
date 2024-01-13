import telebot

from App.Bot.Markups import MarkupBuilder
from App.Config import bot
from App.Config import message_context_manager
from App.Config import sessions_dirPath
from App.Database.DAL.AccountDAL import AccountDAL
from App.Database.session import async_session

async def _stories(message):

    msg = await bot.send_message(message.chat.id, 
        MarkupBuilder.serviceMenuText,
        reply_markup=MarkupBuilder.StoriesMenu(),
        parse_mode="MarkdownV2"
    )
    
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

