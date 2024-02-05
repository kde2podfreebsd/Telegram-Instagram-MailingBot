from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import and_

from App.Database.Models.Models import AccountStories, PremiumChatMember
from App.Database.DAL.ChatMemberDAL import ChatMemberDAL
from App.Logger import ApplicationLogger

from App.UserAgent.UserAgentDbPremiumUsers import get_members_from_tg
import os

import asyncio
from App.Database.session import async_session
from App.Config import sessions_dirPath

logger = ApplicationLogger()

class AccountStoriesDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def getAccountBySessionName(self, session_name):
        result = await self.db_session.execute(
            select(AccountStories).filter(
                AccountStories.session_file_path.ilike(f"%{session_name}.session")
            )
        )
        return result.scalar()

    async def createAccountStories(self, session_name):
        try:
            session_file_path = os.path.join(sessions_dirPath, f"{session_name}.session")
            account_stories = AccountStories(
                session_file_path=session_file_path,
            )
            self.db_session.add(account_stories)
            await self.db_session.flush()
            return account_stories
        except IntegrityError:
            await self.db_session.rollback()
            logger.log_warning("IntegrityError, db rollback")
            return None
    
    async def addTargetChannel(self, session_name, username):
        account_stories = await self.getAccountBySessionName(session_name)
        async with async_session() as session:
            chat_member_dal = ChatMemberDAL(session)
            if account_stories:
                if account_stories.target_channels is None:
                    account_stories.target_channels = []
                    logger.log_info("Init Mutable ARRAY = []")

                if username not in account_stories.target_channels:
                    try:
                        premium_users = await get_members_from_tg(
                            session_name=session_name,
                            usernames=[username[1:]]
                        )
                    except Exception as e:
                        logger.log_error(f"An error occured while adding a target channel to {session_name} AccountStories: {e}")
                        return str(e)
                    else:
                        account_stories.target_channels.append(username)
                        self.db_session.add(account_stories)
                        await self.db_session.flush()
                        logger.log_info(
                            f"{username} added to {session_name}.target_channels"
                        )
                        for premium_user in premium_users:
                            await chat_member_dal.createChatMember(
                                username=premium_user, 
                                account_stories_id=account_stories.id,
                                target_channel=username
                            )
                        return True
                else:
                    logger.log_warning(f"{username} already exists in {session_name}'s target channels")
                    return "Target channel already exists in data base"
            else:
                logger.log_error(
                    "AccountStories doesnt exists in database or target channel already in account.target_channels"
                )
                return False

    async def removeTargetChannel(self, session_name, username):
        account_stories = await self.getAccountBySessionName(session_name)
        if account_stories and account_stories.target_channels:
            if username in account_stories.target_channels:
                async with async_session() as session:
                    chat_member_dal = ChatMemberDAL(session)
                    id = account_stories.id
                    chat_members = await self.db_session.execute(select(PremiumChatMember).filter(
                            and_(
                                PremiumChatMember.account_stories_id == id,
                                PremiumChatMember.target_channel == username
                            )
                        )
                    )
                    for chat_member in chat_members.scalars():
                        await chat_member_dal.deleteChatMemberByIdAndTargetChannel(
                            username=chat_member.username,
                            account_stories_id=id,
                            target_channel=username
                        )
                account_stories.target_channels.remove(username)
                if len(account_stories.target_channels) == 0:
                    account_stories.status = False
                await self.db_session.flush()
                logger.log_info(
                    f"{username} removed from {session_name}.target_channels"
                )
                return True
        logger.log_error(
            "AccountStories doesnt exists in database or target channel not in account_stories_dal.target_channels"
        )
        return False
    
    async def deleteAccountStories(self, session_name):
        account_stories = await self.getAccountBySessionName(session_name)
        if account_stories:
            target_channels = account_stories.target_channels
            if target_channels:
                for target_channel in target_channels:
                    await self.removeTargetChannel(
                        session_name=session_name, 
                        username=target_channel
                    )
            await self.db_session.delete(account_stories)
            await self.db_session.flush()
            logger.log_info(f"AccountStories {session_name} has been removed from the data base")
            return True
        else:
            logger.log_error("AccountStories doesn't exist in database")
            return False

    async def getPremiumMemebers(self, account_stories_id):
        async with async_session() as session:
            chat_member_dal = ChatMemberDAL(session)
            result = await chat_member_dal.db_session.execute(select(PremiumChatMember).filter(PremiumChatMember.account_stories_id == account_stories_id))
            return [member.username for member in result.scalars()]
        
    async def getAllAccounts(self):
        result = await self.db_session.execute(select(AccountStories))
        return [row[0] for row in result]
    
    async def updateDelay(self, session_name, new_delay):
        account = await self.getAccountBySessionName(
            session_name=session_name
        )
        if account:
            account.delay = new_delay
            await self.db_session.commit()
            logger.log_info(f"AccountStories {session_name}'s delay has been changed to {new_delay}")
        else:
            logger.log_error(f"AccountStories {session_name} does not exist in data base")

    async def updateStatus(self, session_name, new_status):
        account = await self.getAccountBySessionName(
            session_name=session_name
        )
        if account:
            account.aioscheduler_status = new_status
            await self.db_session.commit()
            logger.log_info(f"AccountStories {session_name}'s status has been changed to {new_status}")
        else:
            logger.log_error(f"AccountStories {session_name} does not exist in data base")
    
    async def getSessionNamesWithTrueStatus(self):
        result = await self.db_session.execute(
            select(AccountStories.session_file_path).filter(AccountStories.aioscheduler_status == True)
        )
        session_paths = [row[0] for row in result]
        session_names = [
            os.path.splitext(os.path.basename(path))[0] for path in session_paths
        ]
        return session_names
        

async def main():
    async with async_session() as session:
        account_stories_dal = AccountStoriesDAL(session)
        # await account_stories_dal.create_account_stories(f"{sessions_dirPath}/test.session")
        # result = await account_stories_dal.getAccountBySessionName("test")
        # print(result)
        r = await account_stories_dal.deleteAccountStories("test")
        print(r)

if __name__ == "__main__":
    asyncio.run(main())