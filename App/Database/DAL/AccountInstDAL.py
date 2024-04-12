import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import and_

from App.Config import inst_sessions_dirPath
from App.Database.Models.Models import AccountInst, Follower
from App.Logger import ApplicationLogger
from App.Database.DAL.FollowerDAL import FollowerDAL
from App.Database.DAL.ProxyDAL import ProxyAddressDAL
from App.Parser.InstagramParser import InstagramParser

logger = ApplicationLogger()


import asyncio
from App.Database.session import async_session

class AccountInstDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def getAccountBySessionName(self, session_name):
        result =  await self.db_session.execute(
            select(AccountInst).filter(
                AccountInst.session_file_path.ilike(f"%{session_name}.cookies")
            )
        )
        return result.scalar()

    async def createAcount(
        self,
        session_name,
        target_channel=None,
        message=None,
    ):
        session_file_path = os.path.join(inst_sessions_dirPath, f"{session_name}.cookies")

        if not os.path.isfile(session_file_path):
            logger.log_error(f"Not found cookies file with this name {session_name}")
            return None

        try:
            existing_account = await self.getAccountBySessionName(session_name)
            if existing_account:
                logger.log_error(f"AccountInst already exist with this name {session_name}")
                return None

            account = AccountInst(
                session_file_path=session_file_path,
                target_channels=target_channel,
                message=message,
            )
            self.db_session.add(account)
            await self.db_session.flush()

            logger.log_info(f"AccountInst {session_name} added to database")
            return account

        except IntegrityError:
            await self.db_session.rollback()
            logger.log_warning("IntegrityError, db rollback")
            return None
    
    async def addTargetInstChannel(self, target_channel, session_name):
        account = await self.getAccountBySessionName(
            session_name=session_name
        )
        async with async_session() as session:
            follower_dal = FollowerDAL(session)
            proxy_dal = ProxyAddressDAL(session)
            proxies = await proxy_dal.getProxyAddressById(
                account_inst_id=account.id
            )
            instagramParser = InstagramParser(
                login=session_name,
                password="null",
                proxy=proxies[0]
            )

            if (account):
                if account.target_channels is None:
                    account.target_channels = []
                    logger.log_info("Init Mutable ARRAY = []")
                
                if target_channel not in account.target_channels:
                    followers = await instagramParser.async_parse_follower(channel=target_channel)
                    if (isinstance(followers, list)):
                        account.target_channels.append(target_channel)
                        self.db_session.add(account)
                        await self.db_session.flush()
                        logger.log_info(
                            f"{target_channel} added to {session_name}.target_channels"
                        )
                        for follower in followers:
                            await follower_dal.createFollower(
                                username=follower,
                                account_inst_id=account.id,
                                target_channel=target_channel
                            )
                    else:
                        logger.log_error(f"An error occured while parsing {target_channel}'s followers: either followers are private or selenium didn't parse website properly")
                        return False
                else:
                    logger.log_warning(f"{target_channel} already exists in {session_name}'s target channels")
                    return "Target channel already exists in data base"
                return True
            else:
                logger.log_error(
                    "AccountInst doesnt exists in database or target channel already in account.target_channels"
                )
                return False

    async def removeTargetChannel(self, session_name, target_channel):
        account = await self.getAccountBySessionName(session_name)
        if account and account.target_channels:
            if target_channel in account.target_channels:
                async with async_session() as session:
                    follower_dal = FollowerDAL(session)
                    id = account.id
                    followers = await self.db_session.execute(select(Follower).filter(
                            and_(
                                Follower.account_inst_id == id,
                                Follower.target_channel == target_channel
                            )
                        )
                    )
                    for follower in followers.scalars():
                        await follower_dal.deleteFollowerByIdAndTargetChannel(
                            username=follower.username,
                            account_inst_id=id,
                            target_channel=target_channel
                        )
                account.target_channels.remove(target_channel)
                if (len(account.target_channels) == 0):
                    account.status = False
                await self.db_session.flush()
                logger.log_info(
                    f"{target_channel} removed from {session_name}.target_channels"
                )
                return True
        logger.log_error(
            "AccountInst doesnt exists in database or target channel not in account_inst_dal.target_channels"
        )
        return False

    async def updateMessage(self, session_name, new_message):
        account = await self.getAccountBySessionName(session_name)
        if account:
            account.message = new_message
            await self.db_session.flush()
            logger.log_info(f"Updated message: {new_message} on AccountInst {session_name}")
            return True
        else:
            logger.log_error("Account doesnt exists in database")
            return False
    
    async def deleteAccountInst(self, session_name):
        account_inst = await self.getAccountBySessionName(session_name)
        if account_inst:
            target_channels = account_inst.target_channels
            if target_channels:
                for target_channel in target_channels:
                    await self.removeTargetChannel(
                        session_name=session_name, 
                        target_channel=target_channel
                    )

            async with async_session() as session:
                proxy_dal = ProxyAddressDAL(session)
                proxies = await proxy_dal.getProxyAddressById(account_inst_id=account_inst.id)
                if proxies:
                    for proxy in proxies:
                        await proxy_dal.deleteProxyAddress(
                            address=proxy,
                            account_inst_id=account_inst.id
                        )

            await self.db_session.delete(account_inst)
            await self.db_session.flush()

            os.remove(path=f"{inst_sessions_dirPath}/{session_name}.cookies")

            logger.log_info(f"AccountInst {session_name} has been removed from the data base")
            return True
        else:
            logger.log_error("AccountInst doesn't exist in database")
            return False
    
    async def updateStatus(self, session_name, new_status):
        account = await self.getAccountBySessionName(
            session_name=session_name
        )
        if account:
            account.status = new_status
            await self.db_session.commit()
            logger.log_info(f"AccountInst {session_name}'s status has been changed to {new_status}")
            return True
        else:
            logger.log_error(f"AccountInst {session_name} does not exist in data base")
            return False
    
    async def updateDelay(self, session_name, new_delay):
        account = await self.getAccountBySessionName(
            session_name=session_name
        )
        if account:
            account.delay = new_delay
            await self.db_session.commit()
            logger.log_info(f"AccountInst {session_name}'s delay has been changed to {new_delay}")
            return True
        else:
            logger.log_error(f"AccountInst {session_name} does not exist in data base")
            return False
    
    async def updateReelsLink(self, session_name, new_reels_link):
        account = await self.getAccountBySessionName(
            session_name=session_name
        )
        if account:
            account.reels_link = new_reels_link
            await self.db_session.commit()
            logger.log_info(f"AccountInst {session_name}'s reels link has been changed to {new_reels_link}")
            return True
        else:
            logger.log_error(f"AccountInst {session_name} does not exist in data base")
            return False
    
    async def getSessionNamesWithTrueStatus(self):
        result = await self.db_session.execute(
            select(AccountInst.session_file_path).filter(AccountInst.status == True)
        )
        session_paths = [row[0] for row in result]
        session_names = [
            os.path.splitext(os.path.basename(path))[0] for path in session_paths
        ]
        return session_names

    async def getAllAccounts(self):
        result = await self.db_session.execute(select(AccountInst))
        return [row[0] for row in result]
    
    async def getFollowers(self, account_inst_id):
        async with async_session() as session:
            follower_dal = FollowerDAL(session)
            result = await follower_dal.db_session.execute(select(Follower).filter(Follower.account_inst_id == account_inst_id))
            return [member.username for member in result.scalars()]
    
    async def getAllFollowers(self):
        async with async_session() as session:
            follower_dal = FollowerDAL(session)
            result = await follower_dal.db_session.execute(select(Follower))
            return [{"username": member.username, "id": member.account_inst_id} for member in result.scalars()]
    
async def main():
    async with async_session() as session:
        x = AccountInstDAL(session)
        account = await x.getAccountBySessionName(session_name="ivanov.stuff@mail.ru")
        result = await x.getSessionNamesWithTrueStatus()
        print(result)

if __name__ == "__main__":
    asyncio.run(main())