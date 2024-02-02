from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.Database.Models.Models import TargetChannel
from App.Database.DAL import AccountTgDAL

from App.Logger import ApplicationLogger

from App.UserAgent.UserAgentDbPremiumUsers import get_members_from_tg


from App.Database.session import async_session
import asyncio

logger = ApplicationLogger()

class TargetChannelDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_target_channel(self, username, session_name):
        try:
            target_channel = TargetChannel(username=username)
            result = await get_members_from_tg(
                session_name=session_name, 
                usernames=[username[1:]]
            )
            try:
                target_channel.premium_members = result 
                self.db_session.add(target_channel)
                await self.db_session.flush()
                return target_channel

            except IntegrityError:
                await self.db_session.rollback()
                logger.log_warning("IntegrityError, db rollback")
                return None
            
        except Exception as e:
            logger.log_error(f"An error occured while creating a TargetChannel: {e}")
            return str(e)


    async def delete_target_channel(self, username):
        target_channel = await self.get_target_channel_by_username(username)
        if target_channel:
            await self.db_session.delete(target_channel)
            await self.db_session.flush()
            logger.log_info(f"TargetChannel {username} has been removed from the data base")
            return True
        else:
            logger.log_error("TargetChannel doesn't exist in database")
            return False

    async def get_target_channel_by_username(self, username):
        result = await self.db_session.execute(select(TargetChannel).filter_by(username=username))
        return result.scalar()
    
    async def get_premium_members(self):
        premium_members = await self.db_session.execute(select(TargetChannel.premium_members))
        table = [value for value in premium_members.scalars()]
        return [premium_member for target_channel in table for premium_member in target_channel]

async def main():
    async with async_session() as session:
        x = TargetChannelDAL(session)
        result = await x.get_premium_members()
        print(result)


if __name__ == "__main__":
    asyncio.run(main())