from App.Bot.Markups import MarkupBuilder

from App.Config import bot
from App.Config import message_context_manager
from App.Config import sessions_dirPath
from App.Config import account_context

from App.Logger import ApplicationLogger

from App.Database.DAL.AccountTgDAL import AccountDAL
from App.Database.DAL.ChatMemberDAL import ChatMemberDAL
from App.Database.session import async_session

from App.UserAgent.UserAgentDbPlugin import get_members_from_tg
from App.UserAgent.Core import UserAgentCore

from telethon.tl import functions
from telethon import types

logger = ApplicationLogger()

async def _updateDb(message):
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

        account_id = await account_dal.getAccountIdBySessionName(file_session_path)
        ad_channels = await account_dal.getAccountAdChannelsById(account_id)

        db = await get_members_from_tg(
            account_name, 
            ad_channels
        )

        chm_dal = ChatMemberDAL(session)
        for chatMember in db:
            await chm_dal.addChatMemberToAccount(
                account_id=account_id,
                first_name=chatMember[0],
                last_name=chatMember[1],
                username=chatMember[2],
                is_premium=chatMember[3]
            )

async def _deleteDb(message):
    chat_id = message.chat.id
    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.deleteDbText,
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

        account_id = await account_dal.getAccountIdBySessionName(file_session_path)
        chm_dal = ChatMemberDAL(session)
        usernames = await chm_dal.getAllChatMembersByAccountId(account_id)
        for username in usernames:
            await chm_dal.removeChatMemberFromAccount(account_id, username)

async def giveReaction(message, usernames):
    chat_id = message.chat.id
    account_name = account_context.account_name[chat_id]
    async with UserAgentCore(account_name).app as client:
        max_ids = await client(functions.stories.GetPeerMaxIDsRequest(
            id=usernames
        ))
        # print([(i, j) for i, j in zip(max_ids, usernames)])
        for username, max_id in zip(usernames, max_ids):
            if (max_id != 0):
                # print(username, max_id)
                await client(functions.stories.ReadStoriesRequest(
                    peer=username,
                    max_id=max_id
                ))
                await client(functions.stories.SendReactionRequest(
                    peer=username,
                    story_id=max_id,
                    reaction=types.ReactionEmoji(
                        emoticon='❤️'
                    ),
                    add_to_recent=True
                ))
        

async def _startStories(message):
    chat_id = message.chat.id
    account_name = account_context.account_name[chat_id]
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.storiesServiceText,
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

        account_id = await account_dal.getAccountIdBySessionName(file_session_path)
        chm_dal = ChatMemberDAL(session)
        usernames = await chm_dal.getAllChatMembersByAccountId(account_id)
        # print(usernames)
        await giveReaction(message, usernames)





