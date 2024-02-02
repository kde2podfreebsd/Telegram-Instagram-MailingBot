import os
import re

from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup

from App.Bot.Handlers.EditAccountsMenuHandler import _editAccountsMenu
from App.Bot.Handlers.EditAccountsMenuHandler import _showAccountActions
from App.Bot.Markups import MarkupBuilder
from App.Config import account_context
from App.Config import bot
from App.Config import message_context_manager
from App.Config import inst_sessions_dirPath
from App.Database.DAL.AccountInstDAL import AccountInstDAL
from App.Database.session import async_session


class EditAccountActionStates(StatesGroup):
    UpdateMessage = State()
    EditPrompt = State()
    AddAdvChat = State()
    RemoveAdvChat = State()
    ChangeTargetChat = State()
    ChangeStatus = State()
    DeleteAccount = State()


# --------------Change Message--------------


async def _sendUpdateMessageText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.sendUpdateMessageText,
        reply_markup=MarkupBuilder.back_to_edit_menu(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountActionStates.UpdateMessage)


@bot.message_handler(state=EditAccountActionStates.UpdateMessage)
async def edit_message(message):
    async with async_session() as session:
        account_inst_dal = AccountInstDAL(session)

        await message_context_manager.delete_msgId_from_help_menu_dict(
            chat_id=message.chat.id
        )

        await account_inst_dal.updateMessage(
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





# --------------Add advertisement chat--------------


async def _sendAddAdvChatText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.sendAddAdvChatText,
        reply_markup=MarkupBuilder.back_to_edit_menu(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountActionStates.AddAdvChat)


async def _errorSetAdvChat(message):
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
    await bot.set_state(message.chat.id, EditAccountActionStates.AddAdvChat)


@bot.message_handler(state=EditAccountActionStates.AddAdvChat)
async def add_adv_chat(message):
    async with async_session() as session:
        account_inst_dal = AccountInstDAL(session)

        await message_context_manager.delete_msgId_from_help_menu_dict(
            chat_id=message.chat.id
        )

        pattern = r"^@[A-Za-z0-9]+(_[A-Za-z0-9]+)*$"

        if re.match(pattern, message.text):
            await account_inst_dal.addAdvertisingChannel(
                session_name=account_context.account_name[message.chat.id],
                channel_name=message.text,
            )

            await bot.send_message(
                chat_id=message.chat.id,
                text=MarkupBuilder.adv_chat_added,
                parse_mode="HTML",
            )

            await _showAccountActions(
                message=message,
                account_name=account_context.account_name[message.chat.id],
            )

        else:
            await _errorSetAdvChat(message=message)


# --------------Remove advertisement chat--------------


async def _sendRemoveAdvChatText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.sendRemoveAdvChatText,
        reply_markup=MarkupBuilder.back_to_edit_menu(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountActionStates.RemoveAdvChat)


async def _errorRemoveAdvChat(message):
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
    await bot.set_state(message.chat.id, EditAccountActionStates.RemoveAdvChat)


@bot.message_handler(state=EditAccountActionStates.RemoveAdvChat)
async def remove_adv_chat(message):
    async with async_session() as session:
        account_inst_dal = AccountInstDAL(session)

        await message_context_manager.delete_msgId_from_help_menu_dict(
            chat_id=message.chat.id
        )

        pattern = r"^@[A-Za-z0-9]+(_[A-Za-z0-9]+)*$"

        if re.match(pattern, message.text):
            await account_inst_dal.removeAdvertisingChannel(
                session_name=account_context.account_name[message.chat.id],
                channel_name=message.text,
            )

            await bot.send_message(
                chat_id=message.chat.id,
                text=MarkupBuilder.adv_chat_removed,
                parse_mode="HTML",
            )

            await _showAccountActions(
                message=message,
                account_name=account_context.account_name[message.chat.id],
            )

        else:
            await _errorRemoveAdvChat(message=message)


async def _sendDeleteAccountText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.sendDeleteAccountText,
        reply_markup=MarkupBuilder.back_to_edit_menu(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

    await bot.set_state(message.chat.id, EditAccountActionStates.DeleteAccount)


async def _errorDeleteAccountChat(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        "❌ Ошибка удаления аккаунта",
        reply_markup=MarkupBuilder.hide_menu,
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

    await bot.delete_state(message.chat.id, message.chat.id)

    await _showAccountActions(
        message=message, account_name=account_context.account_name[message.chat.id]
    )

@bot.message_handler(state=EditAccountActionStates.DeleteAccount)
async def delete_account(message):
    async with async_session() as session:
        account_inst_dal = AccountInstDAL(session)
        await message_context_manager.delete_msgId_from_help_menu_dict(
            chat_id=message.chat.id
        )
        if message.text == "ДА, ТОЧНО":
            await account_inst_dal.deleteAccount(
                session_name=account_context.account_name[message.chat.id]
            )
            if os.path.exists(
                f"{inst_sessions_dirPath}/{account_context.account_name[message.chat.id]}.session"
            ):
                os.remove(
                    f"{inst_sessions_dirPath}/{account_context.account_name[message.chat.id]}.session"
                )
            await bot.send_message(
                chat_id=message.chat.id,
                text=MarkupBuilder.account_deleted,
                parse_mode="HTML",
            )
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=message.chat.id
            )
            await _editAccountsMenu(message=message)
        else:
            await _errorDeleteAccountChat(message=message)


# --------------Edit account status--------------
async def _sendChangeStatusMenu(message):
    async with async_session() as session:

        await message_context_manager.delete_msgId_from_help_menu_dict(
            chat_id=message.chat.id
        )
        account_inst_dal = AccountInstDAL(session)
        account = await account_inst_dal.getAccountBySessionName(
            session_name=account_context.account_name[message.chat.id]
        )
        status = account.status
        ready_status = await account_inst_dal.check_account_conditions(
            session_name=account_context.account_name[message.chat.id]
        )

        if not ready_status:
            msg = await bot.send_message(
                chat_id=message.chat.id,
                text=MarkupBuilder.not_ready_change_status(status=status),
                reply_markup=MarkupBuilder.back_to_edit_menu(
                    account_name=account_context.account_name[message.chat.id]
                ),
                parse_mode="HTML",
            )

            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=message.chat.id, msgId=msg.message_id
            )

        else:
            msg = await bot.send_message(
                chat_id=message.chat.id,
                text=MarkupBuilder.ready_change_status(status=status),
                reply_markup=MarkupBuilder.change_status_menu(
                    session_name=account_context.account_name[message.chat.id]
                ),
                parse_mode="HTML",
            )

            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=message.chat.id, msgId=msg.message_id
            )


async def _set_status_on(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        chat_id=message.chat.id,
        text="✅Текущий статус аккаунта: <b>Включен</b>",
        reply_markup=MarkupBuilder.back_to_edit_menu(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )


async def _set_status_off(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        chat_id=message.chat.id,
        text="❌Текущий статус аккаунта: <b>Выключен</b>",
        reply_markup=MarkupBuilder.back_to_edit_menu(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
