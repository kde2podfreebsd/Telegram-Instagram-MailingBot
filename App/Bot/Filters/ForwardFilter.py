from App.Config import bot


@bot.message_handler(is_forwarded=True)
async def forward_filter(message):
    await bot.send_message(message.chat.id, "Бот не принимает пересланые сообщения!")
