import re

from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup

from App.Bot.Handlers.EditAccountsMenuHandler import _showAccountActions
from App.Bot.Markups import MarkupBuilder
from App.Config import account_context
from App.Config import bot
from App.Config import message_context_manager
from App.Database.DAL.AccountDAL import AccountDAL
from App.Database.session import async_session


class EditAccountActionStates(StatesGroup):
    EditMessage = State()
    EditPrompt = State()
    AddAdvChat = State()
    RemoveAdvChat = State()
    ChangeTargetChat = State()
    ChangeStatus = State()
    ReloadChatGPTMessage = State()
    DeleteAccount = State()


# --------------Change Message--------------


async def _sendChangeAccountMessageText(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.sendChangeAccountMessageText,
        reply_markup=MarkupBuilder.back_to_edit_menu(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountActionStates.EditMessage)


@bot.message_handler(state=EditAccountActionStates.EditMessage)
async def edit_message(message):
    async with async_session() as session:
        account_dal = AccountDAL(session)

        await message_context_manager.delete_msgId_from_help_menu_dict(
            chat_id=message.chat.id
        )

        await account_dal.updateMessage(
            session_name=account_context.account_name[message.chat.id],
            new_message=message.text,
        )

        await bot.send_message(
            chat_id=message.chat.id,
            text=MarkupBuilder.message_edited,
            parse_mode="HTML",
        )

        await _showAccountActions(
            message=message, account_name=account_context.account_name[message.chat.id]
        )


# --------------Change Prompt--------------


async def _sendChangePromptText(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.sendChangePromptText,
        reply_markup=MarkupBuilder.back_to_edit_menu(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountActionStates.EditPrompt)


@bot.message_handler(state=EditAccountActionStates.EditPrompt)
async def edit_prompt(message):
    async with async_session() as session:
        account_dal = AccountDAL(session)

        await message_context_manager.delete_msgId_from_help_menu_dict(
            chat_id=message.chat.id
        )

        await account_dal.updatePrompt(
            session_name=account_context.account_name[message.chat.id],
            new_prompt=message.text,
        )

        await bot.send_message(
            chat_id=message.chat.id, text=MarkupBuilder.prompt_edited, parse_mode="HTML"
        )

        await _showAccountActions(
            message=message, account_name=account_context.account_name[message.chat.id]
        )


# --------------Change Target Channel--------------


async def _sendChangeTargetChannelText(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.sendChangePromptText,
        reply_markup=MarkupBuilder.back_to_edit_menu(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountActionStates.ChangeTargetChat)


async def _errorSetTargetChannel(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorSetTargetChannel,
        reply_markup=MarkupBuilder.back_to_edit_menu(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountActionStates.ChangeTargetChat)


@bot.message_handler(state=EditAccountActionStates.ChangeTargetChat)
async def edit_target_chat(message):
    async with async_session() as session:
        account_dal = AccountDAL(session)

        await message_context_manager.delete_msgId_from_help_menu_dict(
            chat_id=message.chat.id
        )

        pattern = r"^@[A-Za-z0-9]+(_[A-Za-z0-9]+)*$"

        if re.match(pattern, message.text):
            await account_dal.updateTargetChat(
                session_name=account_context.account_name[message.chat.id],
                new_target_chat=message.text,
            )

            await bot.send_message(
                chat_id=message.chat.id,
                text=MarkupBuilder.prompt_edited,
                parse_mode="HTML",
            )

            await _showAccountActions(
                message=message,
                account_name=account_context.account_name[message.chat.id],
            )
        else:
            await _errorSetTargetChannel(message=message)
