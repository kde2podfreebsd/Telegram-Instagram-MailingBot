import asyncio

# from App.Database.session import async_session

# from App.Database.DAL.AccountDAL import AccountDAL


async def main():
    # async with async_session() as session:
    pass
    # account_dal = AccountDAL(session)

    # session_name = "donqhomo"
    # target_chat = "@kek"

    # 1. Создание аккаунта
    # account = await account_dal.createAccount(session_name, target_chat)
    # print(account)

    # 2. Обновление целевого чата
    # new_target_chat = "@new_kek"
    # updated = await account_dal.updateTargetChat(session_name, new_target_chat)
    # print(updated)

    # 3. Обновление сообщения
    # new_message = "Hello, world!"
    # updated = await account_dal.updateMessage(session_name, new_message)
    # print(updated)

    # 4. Добавление рекламного канала
    # channel_name = "123"
    # added = await account_dal.addAdvertisingChannel(session_name, channel_name)
    # print(added)
    #

    # 5. Удаление рекламного канала
    # removed = await account_dal.removeAdvertisingChannel(session_name, channel_name)
    # print(removed)
    #
    # account = await account_dal.getAccountBySessionName("donqhomo")
    # print(account.advertising_channels)

    # 6. Удаление аккаунта
    # deleted = await account_dal.deleteAccount(session_name)
    # print(deleted)


if __name__ == "__main__":
    asyncio.run(main())
