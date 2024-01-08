import asyncio

from psycopg2 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.Database.Models.Models import ChatMember
from App.Database.session import async_session
from App.Logger import ApplicationLogger

logger = ApplicationLogger()


class ChatMemberDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def addChatMemberToAccount(
            self,
            account_id: int,
            first_name:str,
            last_name:str,
            username: str,
            is_premium: bool = False
    ):
        existing_user = await self.db_session.execute(select(ChatMember).where(ChatMember.username == username))
        existing_user = existing_user.scalars().first()

        if existing_user:
            logger.log_error(f"Пользователь {username} уже существует в базе данных.")
            return existing_user

        new_chat_member = ChatMember(
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_premium=is_premium,
            account_id=account_id
        )

        self.db_session.add(new_chat_member)
        try:
            await self.db_session.commit()
            return new_chat_member
        except IntegrityError as e:
            logger.log_error(f"Ошибка при добавлении пользователя: {e}")
            await self.db_session.rollback()
            return None

    async def getPremiumMembersFromDB(self):
        query = await self.db_session.execute(select(ChatMember))
        table = query.scalars().all()
        return [chatMember.username for chatMember in table if chatMember.is_premium]


async def main():
    async with async_session() as session:
        cmdal = ChatMemberDAL(session)
        await cmdal.addChatMemberToAccount(account_id=1, username="123", is_premium=True, first_name="ivan", last_name="bogomolov")

if __name__ == "__main__":

    asyncio.run(main())

