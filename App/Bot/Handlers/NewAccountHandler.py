import os

import telebot

from App.Bot.Markups import MarkupBuilder
from App.Config import bot
from App.Config import message_context_manager
from App.Config import sessions_dirPath


async def _newAccountMenu(message):

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
        MarkupBuilder.new_account_state1,
        reply_markup=MarkupBuilder.back_to_menu(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


@bot.message_handler(content_types=["document"])
async def new_document(message: telebot.types.Message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    result_message = await bot.send_message(
        message.chat.id,
        "<i>Скачиваем ваш документ</i>",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    file_name = message.document.file_name

    if not file_name.endswith(".session"):
        msg = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=result_message.id,
            text="<i>Вы отправили файл с неверным расширением. Расширение файла должно оканчиваться на .session</i>",
            reply_markup=MarkupBuilder.back_to_menu(),
            parse_mode="HTML",
        )
        await message_context_manager.add_msgId_to_help_menu_dict(
            chat_id=message.chat.id, msgId=msg.message_id
        )

        return

    file_path = os.path.join(sessions_dirPath, file_name)

    if os.path.exists(file_path):
        msg = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=result_message.id,
            text="<i>Сессия с таким названием уже существует. Попробуйте отправить другой файл сессии</i>",
            reply_markup=MarkupBuilder.back_to_menu(),
            parse_mode="HTML",
        )

        await message_context_manager.add_msgId_to_help_menu_dict(
            chat_id=message.chat.id, msgId=msg.message_id
        )
        return

    file_id_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_id_info.file_path)

    with open(file_path, "wb") as new_file:
        new_file.write(downloaded_file)

    msg = await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=result_message.id,
        text="<i>Сессия сохранена успешно!</i>",
        reply_markup=MarkupBuilder.back_to_menu(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
