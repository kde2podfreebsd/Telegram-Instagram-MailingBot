from sqlalchemy import select
import telebot

from App.Bot.Markups import MarkupBuilder
from App.Bot.Handlers.StoriesMenuHandler import _stories

from App.Config import bot
from App.Config import message_context_manager
from App.Config import sessions_dirPath
from App.Config import account_context

from App.Database.DAL.AccountDAL import AccountDAL
from App.Database.DAL.ChatMemberDAL import ChatMemberDAL
from App.Database.session import async_session
from App.Database.Models import Account

from App.UserAgent.UserAgentDbPlugin import get_members_from_tg


async def _UpdateDb(message):
    chat_id = message.chat.id
    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.updateDbText,
        reply_markup=MarkupBuilder.back_to_stories_menu(account_name=account_name),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    async with async_session() as session:
  
        account_dal = AccountDAL(session)
        file_session_path = f"{sessions_dirPath}/{account_name}.session"
        session_file_paths = await account_dal.db_session.execute(
            select(Account.session_file_path)
        )
        sessions = [file_path[0] for file_path in session_file_paths]
        session_db_index = sessions.index(file_session_path)
        adchannels = await account_dal.db_session.execute(
            select(Account.advertising_channels)
        )
        adchats_list = [channel for channel in adchannels]
        advertising_channels = adchats_list[session_db_index]
        db = await get_members_from_tg(
            account_name, 
            advertising_channels[0]
        )
        chm_dal = ChatMemberDAL(session)
        for chatMember in db:
            await chm_dal.addChatMemberToAccount(
                account_id=session_db_index + 1,
                first_name=chatMember[0],
                last_name=chatMember[1],
                username=chatMember[2],
                is_premium=chatMember[3]
            )
        await _stories(message=message, account_name=account_name)





