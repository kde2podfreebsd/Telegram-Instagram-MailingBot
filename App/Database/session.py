import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select
from App.Database.Models import ChatMember
from DAL.getMembersFromTg import getMembersFromTg

load_dotenv()

POSTGRES_USER = str(os.getenv("POSTGRES_USER"))
POSTGRES_PASSWORD = str(os.getenv("POSTGRES_PASSWORD"))
# POSTGRES_HOST = "db"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5433
POSTGRES_DB = str(os.getenv("POSTGRES_DB"))


DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    execution_options={"isolation_level": "AUTOCOMMIT"}, 
)

async_session = async_sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()

async def addMembersToDB(usernames):
        db = await getMembersFromTg(usernames, 5) # limit = 5
        async with async_session() as session:
            for member in db:
                chatMember = ChatMember()
                try:
                    chatMember.first_name = member[0]
                except TypeError:
                    pass
                try:
                    chatMember.last_name = member[1]
                except TypeError:
                    pass
                try:
                    chatMember.username = member[2]
                except TypeError:
                    pass
                try:
                    chatMember.is_premium = member[3]
                except TypeError:
                    pass
                session.add(chatMember)
            await session.commit()
        await session.close()