import asyncio

from psycopg2 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_

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
        existing_user = await self.db_session.execute(select(ChatMember).where(
                and_(
                    ChatMember.username == username,
                    ChatMember.account_id == account_id
                )
            )
        )
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
    
    async def removeChatMemberFromAccount(
            self,
            account_id: int,
            username: str
    ):
        existing_user = await self.db_session.execute(
            select(ChatMember).where(
                and_(
                    ChatMember.username == username,
                    ChatMember.account_id == account_id
                )
            )
        )
        existing_user = existing_user.scalars().first()

        if not existing_user:
            logger.log_error(f"Пользователь {username} не найден в базе данных.")
            return None

        await self.db_session.delete(existing_user)
        try:
            await self.db_session.commit()
            return existing_user
        except IntegrityError as e:
            logger.log_error(f"Ошибка при удалении пользователя: {e}")
            await self.db_session.rollback()
            return None

    async def removeAllChatMembers(self, account_id):
        usernames = await self.getAllChatMembersByAccountId(account_id)
        for username in usernames:
            await self.removeChatMemberFromAccount(account_id, username)

    async def getAllChatMembersByAccountId(self, account_id):
        result = await self.db_session.execute(
            select(ChatMember).filter(
                ChatMember.account_id == account_id
            )
        )
        table = result.scalars().all()
        
        return [chatMember.username for chatMember in table]


async def main():
    async with async_session() as session:
        cmdal = ChatMemberDAL(session)
        await cmdal.addChatMemberToAccount(account_id=1, username="coldbaget", is_premium=True, first_name="ivan", last_name="bogomolov")

if __name__ == "__main__":

    asyncio.run(main())

