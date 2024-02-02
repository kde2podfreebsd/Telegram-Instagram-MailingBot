from App.Bot.Markups import MarkupBuilder
from App.Config import account_context
from App.Config import bot
from App.Config import message_context_manager
from App.Config import pfp_file_path
from App.UserAgent.Core import UserAgentCore
import os

async def _visualConfig(account_name, message):
    account = UserAgentCore(account_name)

    avatar_link = await account.downloadProfilePhoto()
    isProfilePicture = (True if avatar_link.split("/")[-1] != "None" else False)

    if isProfilePicture:
        await account.uploadPhoto(avatar_link)
        with open(pfp_file_path, "rb") as photo:
            msg_list = await MarkupBuilder.visualConfigText(
                account_name=account_name, 
                isProfilePicture=isProfilePicture
            )
            for x in range(len(msg_list)):
                if x + 1 == len(msg_list):
                    msg = await bot.send_message(
                        chat_id=message.chat.id,
                        text=msg_list[x],
                        parse_mode="MARKDOWN"
                    )
                    photo_msg = await bot.send_photo(
                        chat_id=message.chat.id,
                        reply_markup=MarkupBuilder.EditVisualOptions(
                            account_name=account_name
                        ),
                        photo=photo
                    )
                    
                    await message_context_manager.add_msgId_to_help_menu_dict(
                        chat_id=message.chat.id, msgId=[msg.message_id, photo_msg.message_id]
                    )
                else:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=msg_list[x],
                        parse_mode="MARKDOWN",
                    )
            os.remove(pfp_file_path)
    else:
        msg_list = await MarkupBuilder.visualConfigText(
            account_name=account_name, 
            isProfilePicture=isProfilePicture
        )
        for x in range(len(msg_list)):
            if x + 1 == len(msg_list):
                msg = await bot.send_message(
                    chat_id=message.chat.id,
                    text=msg_list[x],
                    reply_markup= MarkupBuilder.EditVisualOptions(
                        account_name=account_name
                    ),
                    parse_mode="MARKDOWN"
                )
                
                await message_context_manager.add_msgId_to_help_menu_dict(
                    chat_id=message.chat.id, msgId=[msg.message_id]
                )
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=msg_list[x],
                    parse_mode="MARKDOWN",
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


