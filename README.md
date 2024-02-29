# 🤖 Telegram Mailing Bot for Telegram and Instagram

Этот проект представляет собой Telegram бота, который имеет несколько функций для управления рекламным контентом и таргетированными рассылками. Вот основные функции бота:

* рассылка о рекламируемом канале юзерам телеграм в публичные чаты с возможностью перегенерирования сообщения с 
помощью GPT моделей
* просмотр сториз у пользователей таргетных каналов, имеющих Telegram Premium
* рассылка сообщений и reels в Instagram

# 👀 Посмотри, как бот работает

Перейди вот по этой ссылке 👉 [[Видео презентация]](https://youtu.be/uf7YYGz7lQo) 👈

# ⚙️ Установка и настройка проекта 

## 1. Склонируйте репозиторий с github
```.sh
git clone <https://.git>
```

## 2. Создайте ``` .env ```
```.env
# Database config
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tg

# PGAdmin config
PGADMIN_DEFAULT_EMAIL=root@root.com
PGADMIN_DEFAULT_PASSWORD=root

# Telegram bot
TELEGRAM_BOT_TOKEN= {insert yours here}

# YandexGPT
YANDEX_CLOUD_API_KEY= {insert yours here}
CATALOG_ID_YANDEX_CLOUD= {insert yours here}
```

## 3. Установите необходимые зависимости:
```.sh
❯ python -m venv venv
❯ soruce venv/bin/activate
❯ pip install -r requirements.txt
or
❯ poetry install
```

## 4. Docker start
```.sh
# clear docker cache
❯ sudo docker stop $(sudo docker ps -a -q)
❯ sudo docker rm $(sudo docker ps -a -q)
# Up postgresql database in docker
❯ docker-compose -f docker-compose.yaml build
❯ docker-compose -f docker-compose.yaml up
``` 

## 5. Database setup

1. Alembic init
```.shell
❯ cd Database
❯ rm alembic.ini
❯ rm -rf migrations/
❯ alembic init migrations
```

2. Изменить sqlalchemy.url в alembic.ini
```shell
❯ docker inspect pgdb | grep IPAddress
            "SecondaryIPAddresses": null,
            "IPAddress": "",
                    "IPAddress": "172.22.0.2",

// alembic.ini                
sqlalchemy.url = postgresql://root:root@172.22.0.2:5432/root
//or
sqlalchemy.url = postgresql://root:root@tg:5432/root
```

3. Изменить target_metadata в migrations/env.py
```.python
from Database.Models import Base
target_metadata = Base.metadata
```

4. Создать миграцию
```.shell
❯ alembic revision --autogenerate -m 'init'
```

5. Залить миграцию
```.shell
❯ alembic upgrade heads
```

## 6. Запуск проекта 

1. Создать 4 терминала и прописать в них команду 
```.python
❯ export PYTHONPATH=$PYTHONPATH:$(pwd)
```
2. Прописать по команде в каждом из терминалов
```.python
python3 App/Bot/main.py
```
```.python
python3 App/UserAgent/UserAgentSpamPlugin.py
```
```.python
python3 App/UserAgent/UserAgentStoriesPlugin.py
```
```.python
python3 App/Parser/ParserSpamPlugin.py
```
❗️*Обязательно прописывать команды из корневой директории проекта*

# 📚 Структура телеграм бота, его классы и их методы
## Bot
Содержит папки:  

```Filters```: message_handler'ы по обработке отправки пересланных сообщений или ответа на них 

```Handlers```: меню бота, основная логика взаимодействия с ним

```Markups```: все markup'ы

```Middlewares```: обработка отправки слишком большого количества запросов боту

```main.py```: запуск бота

## Config
```bot.py```: инициализация объекта bot класса AsyncTelebot по ```TELEGRAM_BOT_TOKEN```

```__init__.py```: 

**singleton**: обертка классов, обеспечивающая создание только одного его экземпляра и предоставляющая
глобальную точку доступа к нему

---

**MessageContextManager**: класс, позволяющий хранить id последнего сообщения с помощью chat_id, по которому происходит его удаление

**help_menu_msgId_to_delete** - поля класса, представляющее собой словарь по chat_id id сообщений

**add_msgId_to_help_menu_dict(self, chat_id, msgId)** - добавление id сообщения в help_menu_msgId_to_delete по chat_id

**delete_msgId_from_help_menu_dict(self, chat_id)** - удаление id сообщения в help_menu_msgId_to_delete по chat_id

---

**AccountContext**: класс, позволяющий хранить название аккаунта, с которого происходит взаимодействие с ботом по chat_id

**account_name** - поля класса, представляющее собой словарь по chat_id account_name

**updateAccountName(self, chat_id: int, account_name: str)** - обновление account_name по chat_id в account_name

---

**LoginPasswordContext**: класс, позволяющий хранить логин и пароль по chat_id

**password** - поля класса, представляющее собой словарь по chat_id password

**login** - поля класса, представляющее собой словарь по chat_id login

**updateLogin(self, chat_id: int, login: str)** - обновление login по chat_id в login

**updatePassword(self, chat_id: int, password: str)** - обновление password по chat_id в password

## Database
Содержит папки и файлы: 

```DAL```, 

```Models```,

```session.py``` (конфигурационный файл базы данных, создание движка для взаимодействия с ней)

## Logger

Содержит файлы: 

```ApplicationLogger.py```: создание класса ApplicationLogger

## Parser

Содержит папки и файлы:

```sessions```: папка для дампа куки файлов аккаунтов инстаграм

```InstagramParser.py```:

**InstagramParserExceptions**: класс исключений, который происходят при работе парсера с instagram.com

---

**InstagramParser**: класс, наследуемый от класса Parser, отвечающий за парсинг веб сайта instagram.com

**login, password, proxy** - поля класса, отвечающие за хранение строк логин, пароля и прокси адреса соотвественно

**check_proxy(self)** - метод для проверки подключения к введенному прокси серверу 

**async_check_proxy(self)** - асинхронный метод обертка для check_proxy

**logging_in(self)** - метод, производящий логин в аккаунт Instagram 

**async_logging_in(self)** - асинхронный метод обертка для logging_in

**parse_followers(self, channel: str)** - метод, производящий парсинг фолловеров аккаунта с именем channel

**scroll_followers_dialogue(self, dialogue, followers_count, step=12)** - метод, листающий диалоговое окно с подписчиками канала;
dialogue - объект страницы, followers_count - количество подписчиков, step=12 - количество пролистываемых подписчиков за каждый скрол

**async_parse_follower(self, channel: str)** - асинхронный метод обертка для parse_followers

**send_message(self, message: str, reels_link: str, channel: str)** - метод, отправляющий аккаунту с именем channel message и reels_link

**async_send_message(self, message: str, reels_link: str, channel: str)** - асинхронный метод обертка для send_message

**dump_cookies(self)** - метод для дампа куки файлов 

**load_cookies(self)** - метод для загрузки куки файлов 

---

❗️Если на компьютере установлен веб браузер Chrome, то важно помнить, чтобы он был последней версии, иначе будут происходить конфликты с webdriver_manager. Также, после каждого официального обновления браузера нужно обновлять undetected-chromedriver во избежании ошибок
```.python
# error: urllib.error.HTTPError: HTTP Error 404: Not Found
# fix:
pip install --upgrade undetected-chromedriver
```

---

```Parser.py```:

**Parser** - родительский класс, предоставляющий глобальную точку доступа и гарантирующий, что будет создан только один его экземпляр

**__init__** - инициализация объекта класса

**close_parser(self)** - закрытия веб ресурсов, связанных с классом, таких как веб драйвер

Для тестирования бота с GUI закомменитруйте данные строчки:

```.python
# в __init__
self.__op.add_argument("--no-sandbox") 
self.__op.add_argument("--disable-dev-shm-usage")
self.__op.add_argument(f"--log-path=parser.log")
self.__display = Display(visible=True, size=(1234, 1234))
self.__display.start()
# в close_parser
self.__display.stop()
```

---

```ParserSpamPlugin.py```: плагин, отвечающий за спам рассылку Instagram

```ProxyExtension.py```: создает класс ProxyExtension и подгружает .json файл с введенным прокси, как разрешение браузера

```Xpath.py```: содержит XPATH к объектам страниц, c которых происходит парсинг

## UserAgent

### Core

```UserAgentCore.py```: класс UserAgent и его методы, как обертки над методами pytelegrambotapi

---

Содержит файлы:

```UserAgentDbPremiumUsers.py```:

**DbPremiumExceptions** - класс исключений, который происходят при работе парсера с Telegram

**WRONG_USERNAME_EXCEPTION** - api telegram не смог найти юзера с введенным username'ом

**ADMIN_PRIVILEGES_EXCEPTION** - фолловеры канала, юзернейм которого был введен, не доступны всем пользователям, а только админам

---

**get_members_from_tg(session_name, usernames, limit=None)** - функция для парсинга премиум подписчиков из каналов с usernames для аккаунт с session_name

```UserAgentSpamPlugin.py```: плагин, отвечающий за спам рассылку Telegram

```UserAgentStoriesPlugin.py```: плагин, отвечающий за отслеживание сториз в Telegram

## YandexGPT

Содержит папки и файлы:

```json_history```: папка для хранения логов запросов различных аккаунтов к YandexGPT

```YandexGTPMsgRebuilder.py```:

**YandexGTPMsgRebuilder** - класс конфигурирующий запросы к YandexGPT

**rewrite_message(cls, account_name: str, prompt: str)** - метод, отправляющий YandexGPT сообщение о перегенарации текущего сообщения, согласно промпту 

# Authors

* [@complicat9d](https://github.com/complicat9d)

* [@kde2podfreebsd](https://github.com/kde2podfreebsd)


