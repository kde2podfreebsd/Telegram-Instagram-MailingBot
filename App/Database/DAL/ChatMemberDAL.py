from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.Database.Models.Models import ChatMember
from App.Logger import ApplicationLogger
from getMembersFromTg import getMembersFromTg

logger = ApplicationLogger()

class ChatMemberDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def getPremiumMembersFromDB(self):
        query = await self.db_session.execute(select(ChatMember))
        table = query.scalars().all()
        return [chatMember.username for chatMember in table if chatMember.is_premium] 

    async def getTableFromDB(self):
        query = await self.db_session.execute(select(ChatMember))
        table = query.scalars().all()
        return [[chatMember.first_name, chatMember.last_name, chatMember.username, chatMember.is_premium] for chatMember in table]          