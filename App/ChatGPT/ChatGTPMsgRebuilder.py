import asyncio
import os

import openai
from dotenv import load_dotenv

from App.Database.DAL.AccountDAL import AccountDAL
from App.Database.session import async_session


class ChatGPTMessageRebuilder:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    @staticmethod
    async def rewrite_message(session_name):
        async with async_session() as session:
            account_dal = AccountDAL(session)
            account = await account_dal.getAccountBySessionName(
                session_name=session_name
            )

            data = list()
            data.append(
                {
                    "role": "user",
                    "content": f"""
Переформулируй и дополни рекламное сообщение.
Не убирай {account.target_chat} из сообщения - это ссылка на рекламируемый чат.
Не добавляй лишних слов в ответ, только сгенерированое рекламное сообщение.
Вот описание канала, оно поможет для переформулировки и дополнения рекламного сообщения: {account.prompt}.
Вот сообщение для редактирования: {account.message}
""",
                }
            )

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=data, temperature=0
            )
            resp = completion["choices"][0]["message"]["content"]

            await account_dal.updateMessage(session_name=session_name, new_message=resp)
