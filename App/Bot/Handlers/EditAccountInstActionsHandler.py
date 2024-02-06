import os
import re

from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup

from App.Parser.InstagramParser import InstagramParserExceptions
from App.Bot.Markups import MarkupBuilder
from App.Config import account_context
from App.Config import bot
from App.Config import message_context_manager
from App.Config import inst_sessions_dirPath
from App.Database.DAL.AccountInstDAL import AccountInstDAL
from App.Database.session import async_session


class EditAccountInstActionStates(StatesGroup):
    UpdateMessage = State()
    AddTargetChannel = State()
    RemoveTargetChannel = State()
    ChangeStatus = State()
    DeleteAccount = State()


async def _sendUpdateMessageText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.sendUpdateMessageInstText,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.UpdateMessage)

async def _errorUpdatingInstMessage(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorUpdatingInstMessage,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.UpdateMessage)

@bot.message_handler(state=EditAccountInstActionStates.UpdateMessage)
async def editMessage(message):
    async with async_session() as session:
        account_inst_dal = AccountInstDAL(session)

        result = await account_inst_dal.updateMessage(
            session_name=account_context.account_name[message.chat.id],
            new_message=message.text,
        )
        if (result):
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=message.chat.id
            )
            msg = await bot.send_message(
                message.chat.id,
                MarkupBuilder.updatedMessageInstText,
                reply_markup=MarkupBuilder.back_to_edit_inst_account(
                    account_name = account_context.account_name[message.chat.id]
                ),
                parse_mode="HTML"
            )
            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=message.chat.id, 
                msgId=msg.message_id
            )
        else:
            await _errorUpdatingInstMessage(message)

async def _sendAddTargetChannelText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.sendAddTargetChannelText,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.AddTargetChannel)

async def _errorTargetInstChannel(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorTargetInstChat,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.AddTargetChannel)

async def _errorDbTargetInstChannel(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorDbTargetInstChannel,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.AddTargetChannel)

async def _errorPageNotFound(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorPageNotFound,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.AddTargetChannel)

@bot.message_handler(state=EditAccountInstActionStates.AddTargetChannel)
async def _addTargetInstChannel(message):

    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )
    channel_username = message.text

    pattern = r"^[A-Za-z0-9]+(_[A-Za-z0-9]+)*$"
    instagramParserExceptions = InstagramParserExceptions()
    if (re.match(pattern, channel_username)):
        async with async_session() as session:
            account_stories_dal = AccountInstDAL(session)
            result = await account_stories_dal.addTargetInstChannel(
                target_channel=channel_username,
                session_name=account_context.account_name[message.chat.id]
            )
            if (str(result) == str(instagramParserExceptions.PageNotFound)):
                await _errorPageNotFound(message)
            elif (result):
                msg = await bot.send_message(
                    message.chat.id,
                    MarkupBuilder.addedInstTargetChannel,
                    reply_markup=MarkupBuilder.back_to_edit_inst_account(
                        account_name = account_context.account_name[message.chat.id]
                    ),
                    parse_mode="HTML"
                )
                await message_context_manager.add_msgId_to_help_menu_dict(
                    chat_id=message.chat.id, 
                    msgId=msg.message_id
                )
            else:
                await _errorDbTargetInstChannel(message)
    else:
        await _errorTargetInstChannel(message)


async def _sendRemoveTargetChannelText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.sendRemoveTargetChannelText,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.RemoveTargetChannel)

async def _errorTargetInstChannelRemoval(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorTargetInstChannelRemoval,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.RemoveTargetChannel)

async def _errorDbNonExistentTargetInstChannel(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorDbNonExistentTargetInstChannel,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

    await bot.set_state(message.chat.id, EditAccountInstActionStates.DeleteAccount)

@bot.message_handler(state=EditAccountInstActionStates.RemoveTargetChannel)
async def removeTargetInstChannel(message):
    async with async_session() as session:
        account_inst_dal = AccountInstDAL(session)

        await message_context_manager.delete_msgId_from_help_menu_dict(
            chat_id=message.chat.id
        )

        pattern = r"^[A-Za-z0-9]+(_[A-Za-z0-9]+)*$"

        if re.match(pattern, message.text):
            result = await account_inst_dal.removeTargetChannel(
                session_name=account_context.account_name[message.chat.id],
                target_channel=message.text,
            )
            if (result):
                msg = await bot.send_message(
                    chat_id=message.chat.id,
                    text=MarkupBuilder.removedInstTargetChannel,
                    reply_markup=MarkupBuilder.back_to_edit_inst_account(
                        account_name=account_context.account_name[message.chat.id]
                    ),
                    parse_mode="HTML",
                )
                await message_context_manager.add_msgId_to_help_menu_dict(
                    chat_id=message.chat.id, msgId=msg.message_id
                )
            else:
                await _errorDbNonExistentTargetInstChannel(message)

        else:
            await _errorTargetInstChannelRemoval(message)

async def _sendDeleteAccountInstText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.sendDeleteAccountInstText,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.DeleteAccount)

async def _errorUnknownDeletionAccountCommand(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorUnknownDeletionAccountCommand,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.DeleteAccount)

async def _errorDbAccountInstRemoval(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorDbAccountInstRemoval,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.delete_state(message.chat.id, message.chat.id)


@bot.message_handler(state=EditAccountInstActionStates.DeleteAccount)
async def deleteAccountInst(message):
    if (message.text == "ДА, ТОЧНО"):
        async with async_session() as session:
            account_inst_dal = AccountInstDAL(session)

            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=message.chat.id
            )

            result = await account_inst_dal.deleteAccountInst(
                session_name=account_context.account_name[message.chat.id]
            )
            if (result):
                msg = await bot.send_message(
                    chat_id=message.chat.id,
                    text=MarkupBuilder.deletedAccountInst,
                    reply_markup=MarkupBuilder.back_to_inst_acc_edit(
                        account_name=account_context.account_name[message.chat.id]
                    ),
                    parse_mode="HTML",
                )
                await message_context_manager.add_msgId_to_help_menu_dict(
                    chat_id=message.chat.id, msgId=msg.message_id
                )
            else:
                await _errorDbAccountInstRemoval(message)
    else:
        await _errorUnknownDeletionAccountCommand(message)

async def _errorNoTargetInstChannels(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorNoTargetInstChannels,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.delete_state(message.chat.id, message.chat.id)

async def _changeStatusAccountInst(message, status):
    async with async_session() as session:
        account_stories_dal = AccountInstDAL(session)
        result = await account_stories_dal.getAccountBySessionName(
            session_name=account_context.account_name[message.chat.id]
        )
        if (result.target_channels == None):
            await _errorNoTargetInstChannels(message)
        elif (len(result.target_channels) == 0):
            await _errorNoTargetInstChannels(message)
        else:
            msg = await bot.send_message(
                message.chat.id,
                MarkupBuilder.changeStatusAccountInst(
                    status=status
                ),
                reply_markup=MarkupBuilder.back_to_edit_inst_account(
                    account_name = account_context.account_name[message.chat.id]
                ),
                parse_mode="HTML"
            )

            await message_context_manager.add_msgId_to_help_menu_dict(
                chat_id=message.chat.id, 
                msgId=msg.message_id
            )
