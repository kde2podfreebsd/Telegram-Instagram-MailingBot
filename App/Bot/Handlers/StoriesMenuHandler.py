from App.Bot.Markups import MarkupBuilder
from App.Config import bot
from App.Config import message_context_manager
from App.Config import account_context

async def _stories(message, account_name):
    msg_list = await MarkupBuilder.showAccountStoriesActions(account_name=account_name)

    for x in range(len(msg_list)):
        if x + 1 == len(msg_list):
            msg = await bot.send_message(
                chat_id=message.chat.id,
                text=msg_list[x],
                reply_markup=MarkupBuilder.StoriesMenu(
                    account_name=account_name
                ),
                parse_mode="MARKDOWN",
            )
            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=message.chat.id, msgId=msg.message_id
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=msg_list[x],
                parse_mode="MARKDOWN",
            )

async def _showAccountStories(message):
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
        reply_markup=await MarkupBuilder.AccountStoriesListKeyboard(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

async def _aioschedulerStoriesMenu(message):
    account_name = account_context.account_name[message.chat.id]
    msg_list = await MarkupBuilder.showAccountStoriesAioschdeulerActions(
        account_name=account_name
    )
    for x in range(len(msg_list)):
        if x + 1 == len(msg_list):
            msg = await bot.send_message(
                chat_id=message.chat.id,
                text=msg_list[x],
                reply_markup=MarkupBuilder.AioshedulerStoriesMenu(
                    account_name=account_name
                ),
                parse_mode="MARKDOWN",
            )
            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=message.chat.id, msgId=msg.message_id
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=msg_list[x],
                parse_mode="MARKDOWN",
            )
