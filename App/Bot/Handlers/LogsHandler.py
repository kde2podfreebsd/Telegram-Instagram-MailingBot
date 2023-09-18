from App.Config import bot
from App.Config import logs_dirPath


async def _sendLog(message):
    with open(f"{logs_dirPath}/app.log", "rb") as log_file:
        await bot.send_document(chat_id=message.chat.id, document=log_file)
