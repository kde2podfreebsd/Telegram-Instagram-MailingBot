import os
import re

from telebot.asyncio_handler_backends import State
from telebot.asyncio_handler_backends import StatesGroup

from App.Parser.InstagramParser import InstagramParserExceptions, InstagramParser
from App.Bot.Markups import MarkupBuilder
from App.Config import account_context
from App.Config import bot
from App.Config import message_context_manager
from App.Config import inst_sessions_dirPath
from App.Database.DAL.AccountInstDAL import AccountInstDAL
from App.Database.DAL.ProxyDAL import ProxyAddressDAL
from App.Database.session import async_session


class EditAccountInstActionStates(StatesGroup):
    UpdateMessage = State()
    AddTargetChannel = State()
    RemoveTargetChannel = State()
    ChangeStatus = State()
    DeleteAccount = State()
    AddProxy = State()
    DeleteProxy = State()
    UpdateReelsLink = State()
    SetDelay = State()

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

async def _errorInsufficientAmountOfProxiesForParsing(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorInsufficientAmountOfProxiesForParsing,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

async def _sendAddTargetChannelText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )
    async with async_session() as session:
        proxy_dal = ProxyAddressDAL(session)
        account_inst_dal = AccountInstDAL(session)
        account = await account_inst_dal.getAccountBySessionName(
            session_name=account_context.account_name[message.chat.id]
        )
        proxies = await proxy_dal.getProxyAddressById(
            account_inst_id=account.id
        )
        amount_of_proxies = len(proxies)
        if (amount_of_proxies < 1):
            await _errorInsufficientAmountOfProxiesForParsing(message)
        else:
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
            msg_filler = await bot.send_message(
                message.chat.id,
                MarkupBuilder.parsingFollowers,
                parse_mode="HTML"
            )
            
            result = await account_stories_dal.addTargetInstChannel(
                target_channel=channel_username,
                session_name=account_context.account_name[message.chat.id]
            )
            await bot.delete_message(
                chat_id=message.chat.id, 
                message_id=msg_filler.id
            )
            if (str(result) == str(instagramParserExceptions.PageNotFound)):
                await _errorPageNotFound(message)
            elif (result and result != []):
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
                    reply_markup=MarkupBuilder.back_to_inst_acc_edit,
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

async def _errorNoMessage(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorNoMessage,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

async def _errorInsufficientAmountOfProxies(message, amount_of_proxies):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorInsufficientAmountOfProxies(
            amount_of_proxies=amount_of_proxies
        ),
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

async def _errorNoMessageAndNoReels(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorNoMessageAndNoReels,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )

async def _changeStatusAccountInst(message, status):
    
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

async def _errorProxyAddress(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorProxyAddress,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.AddProxy)

async def _errorInvalidProxyAdress(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorInvalidProxyAdress,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.AddProxy)

async def _sendAddProxyText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.addProxyText,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.AddProxy)

async def _errorExpiredProxyDb(message):
    chat_id = message.chat.id
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=chat_id
    )
    msg = await bot.send_message(
        message.chat.id,
        text=MarkupBuilder.errorExpiredProxyDb,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(),
        parse_mode="HTML",
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, state = EditAccountInstActionStates.AddProxy)

@bot.message_handler(state=EditAccountInstActionStates.AddProxy)
async def _addProxy(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )
    async with async_session() as session:
        account_inst_dal = AccountInstDAL(session)
        account = await account_inst_dal.getAccountBySessionName(
            session_name=account_context.account_name[message.chat.id]
        )
        proxy = message.text
        proxy_pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+:[A-Za-z0-9]+:[A-Za-z0-9]+)$'
        if (re.match(proxy_pattern, proxy)):
            async with async_session() as session:
                instagramParser = InstagramParser(
                    login="",
                    password="",
                    proxy=proxy
                )
                msg_filler = await bot.send_message(
                    message.chat.id,
                    MarkupBuilder.addingProxy,
                    parse_mode="HTML"
                )
                
                is_proxy_connection_failed = str(await instagramParser.async_check_proxy())
                proxy_connection_failed = str(InstagramParserExceptions().ProxyConnectionFailed)

                await bot.delete_message(message.chat.id, msg_filler.id)

                if (proxy_connection_failed not in is_proxy_connection_failed):
                    proxy_dal = ProxyAddressDAL(session)
                    result = await proxy_dal.createProxyAddress(address=message.text, account_inst_id=account.id)
                    if (result is not None):
                        msg = await bot.send_message(
                            message.chat.id,
                            MarkupBuilder.addedProxyText,
                            reply_markup=MarkupBuilder.back_to_edit_inst_account(
                                account_name=account_context.account_name[message.chat.id]
                            ),
                            parse_mode="HTML",
                        )
                        await message_context_manager.add_msgId_to_help_menu_dict(
                            chat_id=message.chat.id, msgId=msg.message_id
                        )
                        
                    else:
                        await _errorProxyAddress(message)
                else:
                    await _errorExpiredProxyDb(message)
        else:
            await _errorInvalidProxyAdress(message)

async def _sendDeleteProxyText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.deleteProxyAddress,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.DeleteProxy)

async def _errorProxyAddressRemoval(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorProxyAddressRemoval,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.DeleteProxy)

async def _errorInvalidProxyAdressRemoval(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorInvalidProxyAdress,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.DeleteProxy)


@bot.message_handler(state=EditAccountInstActionStates.DeleteProxy)
async def _deleteProxy(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )
    async with async_session() as session:
        account_inst_dal = AccountInstDAL(session)
        account = await account_inst_dal.getAccountBySessionName(
            session_name=account_context.account_name[message.chat.id]
        )
        proxy = message.text
        proxy_pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+:[A-Za-z0-9]+:[A-Za-z0-9]+)$'
        if (re.match(proxy_pattern, proxy)):
            async with async_session() as session:
                proxy_dal = ProxyAddressDAL(session)
                result = await proxy_dal.deleteProxyAddress(
                    address=message.text, 
                    account_inst_id=account.id
                )
                if (result is not None):
                    msg = await bot.send_message(
                        message.chat.id,
                        MarkupBuilder.deletedProxyAddress,
                        reply_markup=MarkupBuilder.back_to_edit_inst_account(
                            account_name=account_context.account_name[message.chat.id]
                        ),
                        parse_mode="HTML",
                    )
                    await message_context_manager.add_msgId_to_help_menu_dict(
                        chat_id=message.chat.id, msgId=msg.message_id
                    )
                    
                else:
                    await _errorProxyAddressRemoval(message)
        else:
            await _errorInvalidProxyAdressRemoval(message)

async def _setDelayForInstText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.setDelayForInstText,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.SetDelay)

async def _errorDelayInst(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorDelayInst,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

    await bot.set_state(message.chat.id, EditAccountInstActionStates.SetDelay)

async def _errorNotIntegerInstDelay(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorNotIntegerInstDelay,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

    await bot.set_state(message.chat.id, EditAccountInstActionStates.SetDelay)

@bot.message_handler(state=EditAccountInstActionStates.SetDelay)
async def _setDelayForInst(message):
    async with async_session() as session:
        account_stories_dal = AccountInstDAL(session)
        new_delay = message.text
        pattern = r'^\d+$'
        if (re.match(pattern, new_delay) and new_delay != '0'):
            result = await account_stories_dal.updateDelay(
                session_name=account_context.account_name[message.chat.id],
                new_delay=int(new_delay)
            )
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=message.chat.id
            )
            if (result):
                msg = await bot.send_message(
                    message.chat.id,
                    MarkupBuilder.delayForInstBeenSetText,
                    reply_markup=MarkupBuilder.back_to_edit_inst_account(
                        account_name=account_context.account_name[message.chat.id]
                    ),
                    parse_mode="HTML"
                )
                await message_context_manager.add_msgId_to_help_menu_dict(
                    chat_id=message.chat.id, 
                    msgId=msg.message_id
                )
            else:
                await _errorDelayInst(message)
        else:
            await _errorNotIntegerInstDelay(message)

async def _updateReelsLinkText(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        chat_id=message.chat.id
    )

    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.updateReelsLinkText,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name=account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML",
    )
    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, msgId=msg.message_id
    )
    await bot.set_state(message.chat.id, EditAccountInstActionStates.UpdateReelsLink)

async def _errorReelsLink(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorReelsLink,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

    await bot.set_state(message.chat.id, EditAccountInstActionStates.UpdateReelsLink)

async def _errorInvalidReelsLink(message):
    await message_context_manager.delete_msgId_from_help_menu_dict(
        message.chat.id
    )
    msg = await bot.send_message(
        message.chat.id,
        MarkupBuilder.errorInvalidReelsLink,
        reply_markup=MarkupBuilder.back_to_edit_inst_account(
            account_name = account_context.account_name[message.chat.id]
        ),
        parse_mode="HTML"
    )

    await message_context_manager.add_msgId_to_help_menu_dict(
        chat_id=message.chat.id, 
        msgId=msg.message_id
    )

    await bot.set_state(message.chat.id, EditAccountInstActionStates.UpdateReelsLink)

@bot.message_handler(state=EditAccountInstActionStates.UpdateReelsLink)
async def _updateReelsLink(message):
    async with async_session() as session:
        account_stories_dal = AccountInstDAL(session)
        reels_link = message.text
        pattern = r"https://www\.instagram\.com/reel/[\w\d_-]+/\?utm_source=ig_web_copy_link"
        if (re.match(pattern, reels_link)):
            result = await account_stories_dal.updateReelsLink(
                session_name=account_context.account_name[message.chat.id],
                new_reels_link=reels_link
            )
            await message_context_manager.delete_msgId_from_help_menu_dict(
                    chat_id=message.chat.id
            )
            if (result):
                msg = await bot.send_message(
                    message.chat.id,
                    MarkupBuilder.updatedReelsLinkText,
                    reply_markup=MarkupBuilder.back_to_edit_inst_account(
                        account_name=account_context.account_name[message.chat.id]
                    ),
                    parse_mode="HTML"
                )
                await message_context_manager.add_msgId_to_help_menu_dict(
                    chat_id=message.chat.id, 
                    msgId=msg.message_id
                )
            else:
                await _errorReelsLink(message)
        else:
            await _errorInvalidReelsLink(message)