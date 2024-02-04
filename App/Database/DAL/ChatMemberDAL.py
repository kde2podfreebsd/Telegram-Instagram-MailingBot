from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.Database.Models.Models import AccountStories, PremiumChatMember
from App.Logger import ApplicationLogger

import asyncio
from App.Database.session import async_session
from App.Config import sessions_dirPath

logger = ApplicationLogger()

class ChatMemberDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def createChatMember(self, username, account_stories_id):
        try:
            premium_chat_member = PremiumChatMember(username=username, account_stories_id=account_stories_id)
            self.db_session.add(premium_chat_member)
            await self.db_session.flush()
            return premium_chat_member
        except IntegrityError:
            await self.db_session.rollback()
            logger.log_warning("IntegrityError, db rollback")
            return None

    async def deleteChatMember(self, username, account_stories_id):
        premium_chat_member = await self.getChatMember(username, account_stories_id)
        if premium_chat_member:
            await self.db_session.delete(premium_chat_member)
            await self.db_session.flush()
            logger.log_info(f"ChatMember {username} has been removed from the data base")
            return True
        else:
            logger.log_error("ChatMember doesn't exist in database")
            return False

    async def getChatMember(self, username, account_stories_id):
        query = select(PremiumChatMember).where(PremiumChatMember.username == username).where(PremiumChatMember.account_stories_id == account_stories_id)
        result = await self.db_session.execute(query)
        return result.scalar()