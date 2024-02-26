import os
import asyncio

from pathlib import Path
import json
import requests
from dotenv import load_dotenv

from App.Database.DAL.AccountTgDAL import AccountDAL
from App.Config import basedir
from App.Database.session import async_session

load_dotenv()


class YandexGPTMessageRebuilder:

    with open("App/YandexGPT/config.json", "r", encoding="utf-8") as file:
        config_json = json.load(file)

    _tokens_per_day: int = config_json['token_per_day_limit']
    _chat_version: str = "gpt"
    _model: str = "yandexgpt-lite"
    _stream: bool = False
    _temperature: float = 0.6
    _max_tokens: int = 2000
    _url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    _headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {os.getenv('YANDEX_CLOUD_API_KEY')}"
    }

    _payload: dict[str: str] = None
    _response: json = None

    async def sync_prompt(cls, account_name: str, prompt: str) -> str:
        chat_history_file = Path(f"{basedir}/YandexGPT/json_history/{account_name}_history.json")
        if chat_history_file.exists():
            with open(chat_history_file, "r", encoding="utf-8") as file:
                messages_history = json.load(file)
        else:
            messages_history = []

        user_prompt = {"role": "user", "text": prompt}
        messages_history.append(user_prompt)

        cls._payload = {
            "modelUri": f"{cls._chat_version}://{os.getenv('CATALOG_ID_YANDEX_CLOUD')}/{cls._model}",
            "completionOptions": {
                "stream": cls._stream,
                "temperature": cls._temperature,
                "maxTokens": cls._max_tokens
            },
            "messages": messages_history
        }

        try:
            cls._response = requests.post(cls._url, headers=cls._headers, json=cls._payload)
            result = cls._response.json()
        except Exception:
            cls._response = requests.post(cls._url, headers=cls._headers, json=cls._payload)
            result = cls._response.json()

        assistant_response = result["result"]["alternatives"][0]["message"]
        messages_history.append(assistant_response)

        with open(chat_history_file, "w", encoding="utf-8") as file:
            json.dump(messages_history, file, ensure_ascii=False, indent=2)

        return assistant_response['text']

async def main():
    account_name = "lol"
    user_prompt_text = f"""
Переформулируй и дополни рекламное сообщение.
Не убирай @complicat9d из сообщения - это ссылка на рекламируемый чат. Если его нет, то обязательно добавь в конец сообщения.
Не добавляй лишних слов в ответ, только сгенерированое рекламное сообщение.
Вот описание канала, оно поможет для переформулировки и дополнения рекламного сообщения: канал по криптоивестингу с свежими прогнозами.
Вот сообщение для редактирования: Самый лучший канал по криптоивестингу, вступай в наш чат @complicat9d
"""
    response = await YandexGPTMessageRebuilder.sync_prompt(YandexGPTMessageRebuilder, account_name=account_name, prompt=user_prompt_text)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())