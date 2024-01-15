import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.Config import sessions_dirPath
from App.Database.Models.Models import Account
from App.Logger import ApplicationLogger

logger = ApplicationLogger()


class AccountDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def createAccount(
        self,
        session_name,
        target_chat=None,
        message=None,
        advertising_channels=None,
        status=False,
    ):
        session_file_path = os.path.join(sessions_dirPath, f"{session_name}.session")

        if not os.path.isfile(session_file_path):
            logger.log_error(f"Not found session with this name {session_name}")
            return None

        try:
            existing_account = await self.getAccountBySessionName(session_name)
            if existing_account:
                logger.log_error(f"Account already exist with this name {session_name}")
                return None

            account = Account(
                session_file_path=session_file_path,
                target_chat=target_chat,
                message=message,
                advertising_channels=advertising_channels,
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

    async def updateTargetChat(self, session_name, new_target_chat):
        account = await self.getAccountBySessionName(session_name)
        if account:
            account.target_chat = new_target_chat
            await self.db_session.flush()
            logger.log_info(
                f"Updated target chat: {new_target_chat} on account {session_name}"
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

    async def updatePrompt(self, session_name, new_prompt):
        account = await self.getAccountBySessionName(session_name)
        if account:
            account.prompt = new_prompt
            await self.db_session.flush()
            logger.log_info(f"Updated prompt: {new_prompt} on account {session_name}")
            return True
        else:
            logger.log_error("Account doesnt exists in database")
            return False

    async def addAdvertisingChannel(self, session_name, channel_name):
        account = await self.getAccountBySessionName(session_name)
        if account:
            if account.advertising_channels is None:
                account.advertising_channels = []
                logger.log_info("Init Mutable ARRAY = []")

            if channel_name not in account.advertising_channels:
                account.advertising_channels.append(channel_name)
                self.db_session.add(account)
                await self.db_session.flush()
                logger.log_info(
                    f"{channel_name} added to {session_name}.advertising_channels"
                )

                return True

        logger.log_error(
            "Account doesnt exists in database or channel name already in account.advertising_channels"
        )
        return False

    async def removeAdvertisingChannel(self, session_name, channel_name):
        account = await self.getAccountBySessionName(session_name)
        if account and account.advertising_channels:
            if channel_name in account.advertising_channels:
                account.advertising_channels.remove(channel_name)
                if len(account.advertising_channels) == 0:
                    account.status = False
                await self.db_session.flush()
                logger.log_info(
                    f"{channel_name} removed from {session_name}.advertising_channels"
                )
                return True
        logger.log_error(
            "Account doesnt exists in database or channel name not in account.advertising_channels"
        )
        return False

    async def updateStatus(self, session_name, status: bool):
        account = await self.getAccountBySessionName(session_name)
        if account:
            account.status = status
            await self.db_session.flush()
            logger.log_info(f"Updated status: {status} on account {session_name}")
            return True
        else:
            logger.log_error("Account doesnt exists in database")
            return False

    async def getAccountIdBySessionName(self, session_name):
        result = await self.db_session.execute(
            select(Account.id).filter(
                Account.session_file_path == session_name
            )
        )
        return result.scalar()

    async def getAccountAdChannelsById(self, account_id):
        result = await self.db_session.execute(
            select(Account.advertising_channels).filter(
                Account.id == account_id
            )
        )
        return result.scalar()

    async def getAccountBySessionName(self, session_name):
        result = await self.db_session.execute(
            select(Account).filter(
                Account.session_file_path.ilike(f"%{session_name}.session")
            )
        )
        return result.scalar()

    async def getSessionNamesWithTrueStatus(self):
        result = await self.db_session.execute(
            select(Account.session_file_path).filter(Account.status == True)
        )
        session_paths = [row[0] for row in result]
        session_names = [
            os.path.splitext(os.path.basename(path))[0] for path in session_paths
        ]
        return session_names

    async def getAllAccounts(self):
        result = await self.db_session.execute(select(Account))
        return [row[0] for row in result]

    async def createAccountsFromSessionFiles(self):
        session_files = os.listdir(sessions_dirPath)

        for session_file in session_files:
            if session_file.endswith(".session"):
                session_name = os.path.splitext(session_file)[0]
                await self.createAccount(session_name=session_name)

    async def check_account_conditions(self, session_name: str):
        account = await self.getAccountBySessionName(session_name)
        if (
            account.target_chat != "Не указан"
            and account.message != "Не указано"
            and account.prompt != "Не указан"
        ):
            if account.advertising_channels and len(account.advertising_channels) > 0:
                if os.path.isfile(account.session_file_path):
                    return True

        return False
