import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage


load_dotenv()

bot = AsyncTeleBot(
    str(os.getenv("TELEGRAM_BOT_TOKEN")),
    state_storage=StateMemoryStorage(),
)
