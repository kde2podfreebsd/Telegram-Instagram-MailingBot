from App.Bot.Markups import MarkupBuilder
from App.Config import account_context
from App.Config import bot
from App.Config import message_context_manager
from App.Config import sessions_dirPath

async def _visualConfig(account_name, message):
    msg = await bot.send_message(message.chat.id, 
        MarkupBuilder.visualConfigText,
        reply_markup=MarkupBuilder.EditVisualOptions(account_name=account_name),
        parse_mode="MarkdownV2"
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


async def _accountSessionsList(message):
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
        reply_markup=await MarkupBuilder.AccountListKeyboardVisCfg(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


