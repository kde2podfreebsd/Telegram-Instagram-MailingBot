import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.Config import inst_sessions_dirPath
from App.Database.Models.Models import AccountInst
from App.Logger import ApplicationLogger

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
        status=False
    ):
        session_file_path = os.path.join(inst_sessions_dirPath, f"{session_name}.cookies")

        if not os.path.isfile(session_file_path):
            logger.log_error(f"Not found cookies file with this name {session_name}")
            return None

        try:
            existing_account = await self.getAccountBySessionName(session_name)
            if existing_account:
                logger.log_error(f"Account already exist with this name {session_name}")
                return None

            account = AccountInst(
                session_file_path=session_file_path,
                target_channel=target_channel,
                message=message,
                status=status,
            )
            self.db_session.add(account)
            await self.db_session.flush()

            logger.log_info("Account added to database")
            return account

        except IntegrityError:
            await self.db_session.rollback()
            logger.log_warning("IntegrityError, db rollback")
            return None
    
    async def deleteAccount(self, session_name):
        account = await self.getAccountBySessionName(session_name)
        if account:
            await self.db_session.delete(account)
            await self.db_session.flush()
            logger.log_info("Account deleted from database")
            return True
        else:
            logger.log_error("Account doesnt exists in database")
            return False
    
    async def updateTargetChannel(self, session_name, new_target_channel):
        account = await self.getAccountBySessionName(session_name)
        if account:
            account.target_channel = new_target_channel
            await self.db_session.flush()
            logger.log_info(
                f"Updated target chat: {new_target_channel} on account {session_name}"
            )
            return True
        else:
            logger.log_error("Account doesnt exists in database")
            return False

    async def updateMessage(self, session_name, new_message):
        account = await self.getAccountBySessionName(session_name)
        if account:
            account.message = new_message
            await self.db_session.flush()
            logger.log_info(f"Updated message: {new_message} on account {session_name}")
            return True
        else:
            logger.log_error("Account doesnt exists in database")
            return False
    
    async def getAllAccounts(self):
        result = await self.db_session.execute(select(AccountInst))
        return [row[0] for row in result]
    
async def main():
    async with async_session() as session:
        x = AccountInstDAL(session)
        result = await x.deleteAccount("ivanov.stuff@mail.ru")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())