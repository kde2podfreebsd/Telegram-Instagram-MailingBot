from App.Bot.Markups import MarkupBuilder
from App.Config import bot
from App.Config import message_context_manager


async def _spamTg(message):

    msg = await bot.send_message(message.chat.id, 
        text=MarkupBuilder.spamTgText,
        reply_markup=MarkupBuilder.SpamTgActionsList(),
        parse_mode="MarkdownV2"
    )
    
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

