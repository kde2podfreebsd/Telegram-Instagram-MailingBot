from App.Config import bot


@bot.message_handler(is_reply=True)
async def reply_filter(message):
    await bot.send_message(message.chat.id, "Бот не принимает ответы на сообщения!")
