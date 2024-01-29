from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import and_

from App.Database.Models.Models import Follower
from App.Database.session import sync_session
from App.Logger import ApplicationLogger

logger = ApplicationLogger()


class FollowerDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def addFollowerToAccountInst(
            self,
            username: str,
            account_inst_id: int
    ):
        existing_user = await self.db_session.execute(select(Follower).where(
                and_(
                    Follower.username == username,
                    Follower.account_inst_id == account_inst_id
                )
            )
        )
        existing_user = existing_user.scalars().first()

        if existing_user:
            logger.log_error(f"Follower {username} already exist in the data base.")
            return existing_user

        new_follower = Follower(
            username=username,
            account_inst_id=account_inst_id
        )

        self.db_session.add(new_follower)
        try:
            await self.db_session.commit()
            return new_follower
        except IntegrityError as e:
            logger.log_error(f"An error occured while adding Follower: {e}")
            await self.db_session.rollback()
            return None
    
    async def removeChatMemberFromAccount(
        self,
        username: str,
        account_inst_id: int
    ):
        existing_user = await self.db_session.execute(
            select(Follower).where(
                and_(
                    Follower.username == username,
                    Follower.account_inst_id == account_inst_id
                )
            )
        )
        existing_user = existing_user.scalars().first()

        if not existing_user:
            logger.log_error(f"Follower {username} has not been found in the data base.")
            return None

        await self.db_session.delete(existing_user)
        try:
            await self.db_session.commit()
            return existing_user
        except IntegrityError as e:
            logger.log_error(f"An error occured while removing Follower: {e}")
            await self.db_session.rollback()
            return None

    async def getAllChatMembersByAccountId(self, account_id):
        result = await self.db_session.execute(
            select(Follower).filter(
                Follower.account_inst_id == account_id
            )
        )
        table = result.scalars().all()
        return [follower.username for follower in table]

    async def removeAllFollowers(self, account_id):
        usernames = await self.getAllChatMembersByAccountId(account_id)
        for username in usernames:
            await self.removeChatMemberFromAccount(account_id, username)




