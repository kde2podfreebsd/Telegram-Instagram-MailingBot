import asyncio

from App.Database.DAL.AccountTgDAL import AccountDAL
from App.Database.session import async_session


async def main():
    async with async_session() as session:
        account_dal = AccountDAL(session)

        # print(await account_dal.getSessionNames())

        session_name = "rhdv"

        # 1. Создание аккаунта
        # account = await account_dal.createAccount(session_name)
        # print(account)

        # await account_dal.updateStatus("donqhomo", True)

        # 2. Обновление целевого чата
        # new_target_chat = "@rhdv"
        # updated = await account_dal.updateTargetChat(session_name, new_target_chat)
        # print(updated)

        # 3. Обновление сообщения


#         new_message = f'''Привет! 🤑
#
# -Хочешь зарабатывать на криптовалюте?
# -Не обязательно иметь опыт!
#
# Ты можешь получать от 30 до 150 долларов в зависимости от своих финансовых возможностей.
#
# Главное - «желание работать и 2-5 часа свободного времени в день».
#
# Жду в {new_target_chat}, подписывайся! 📩💵
# '''
#         updated = await account_dal.updateMessage(session_name, new_message)
# print(updated)

# 4. Добавление рекламного канала
# channel_name = "@publicgrouptesttest"
# added = await account_dal.addAdvertisingChannel(session_name, channel_name)
# print(added)
#

# prompt = "Переформулируй рекламное сообщение, что бы изначальный смысл приблезительно сохранялся. Это реклама канала о криптовалютах, в котором учат зарабатывать на разных направлениях крипты (p2p, трейдинг, сиблинг и тд). Измени как минимум половину сообщения. Обязательно укажи @rhdv как канала для рекламы. Не добавляй лишних слов в ответ, только рекламное сообщение"
# await account_dal.updatePrompt(session_name=session_name, new_prompt=prompt)


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
