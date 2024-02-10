from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import and_

from App.Database.Models.Models import Follower
from App.Logger import ApplicationLogger

logger = ApplicationLogger()


class FollowerDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def createFollower(self, username, account_inst_id, target_channel):
        try:
            existing_account = await self.getFollower(
                username=username, 
                account_inst_id=account_inst_id
            )
            if existing_account:
                logger.log_error(f"Follower with username {username} has already been added to data base")
                return None
            follower = Follower(
                username=username, 
                account_inst_id=account_inst_id,
                target_channel=target_channel
            )
            self.db_session.add(follower)
            await self.db_session.flush()
            return follower
        except IntegrityError:
            await self.db_session.rollback()
            logger.log_warning("IntegrityError, db rollback")
            return None

    async def deleteFollower(self, username, account_inst_id):
        premium_chat_member = await self.getFollower(
            username=username, 
            account_inst_id=account_inst_id
        )
        if premium_chat_member:
            await self.db_session.delete(premium_chat_member)
            await self.db_session.flush()
            logger.log_info(f"Follower {username} has been removed from the data base")
            return True
        else:
            logger.log_error("Follower doesn't exist in database")
            return False
    
    async def deleteFollowerByIdAndTargetChannel(self, username, target_channel, account_inst_id):
        follower = await self.getFollowerByIdAndTargetChannel(
            username=username, 
            target_channel=target_channel, 
            account_inst_id=account_inst_id
        )

        if follower:
            await self.db_session.delete(follower)
            await self.db_session.flush()
            logger.log_info(f"Follower {username} has been removed from the data base")
            return True
        else:
            logger.log_error("Follower doesn't exist in database")
            return False

    async def getFollower(self, username, account_inst_id):
        query = select(Follower).where(Follower.username == username).where(Follower.account_inst_id == account_inst_id)
        result = await self.db_session.execute(query)
        return result.scalar()
    
    async def getFollowerByIdAndTargetChannel(self, username, target_channel, account_inst_id):
        query = select(Follower).where(Follower.username == username).where(
            and_(
                Follower.account_inst_id == account_inst_id,
                Follower.target_channel == target_channel
            )
        )
        result = await self.db_session.execute(query)
        return result.scalar()



