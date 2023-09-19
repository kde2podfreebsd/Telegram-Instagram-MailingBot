import asyncio

from App.Database.DAL.AccountDAL import AccountDAL
from App.Database.session import async_session


async def main():
    async with async_session() as session:
        account_dal = AccountDAL(session)

        # print(await account_dal.getSessionNames())

        session_name = "donqhomo"

        # 1. Создание аккаунта
        # account = await account_dal.createAccount(session_name)
        # print(account)

        # await account_dal.updateStatus("donqhomo", True)

        # 2. Обновление целевого чата
        # new_target_chat = "@new_kek"
        # updated = await account_dal.updateTargetChat(session_name, new_target_chat)
        # print(updated)

        # 3. Обновление сообщения
        # new_message = "Kek lol validol lmaooooooooo!"
        # updated = await account_dal.updateMessage(session_name, new_message)
        # print(updated)

        # 4. Добавление рекламного канала
        # channel_name = "@publicgrouptesttest"
        # added = await account_dal.addAdvertisingChannel(session_name, channel_name)
        # print(added)
        #

        # 5. Удаление рекламного канала
        # removed = await account_dal.removeAdvertisingChannel(session_name, channel_name)
        # print(removed)
        #
        # account = await account_dal.getAccountBySessionName("donqhomo")
        # print(account)

        # 6. Удаление аккаунта
        # deleted = await account_dal.deleteAccount(session_name)
        # print(deleted)

        # 7. Создание аккаунтов из файлов сессий
        # await account_dal.createAccountsFromSessionFiles()


if __name__ == "__main__":
    asyncio.run(main())
