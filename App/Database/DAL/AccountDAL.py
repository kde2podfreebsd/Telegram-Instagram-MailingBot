import os

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from App.Config import sessions_dirPath
from App.Database.Models.Models import Account


class AccountDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def createAccount(
        self, session_name, target_chat, message=None, advertising_channels=None
    ):
        session_file_path = os.path.join(sessions_dirPath, f"{session_name}.session")

        if not os.path.isfile(session_file_path):
            return None

        try:
            async with self.db_session.begin():
                existing_account = await self.getAccountBySessionName(session_name)
                if existing_account:
                    return None

                account = Account(
                    session_file_path=session_file_path,
                    target_chat=target_chat,
                    message=message,
                    advertising_channels=advertising_channels,
                )
                self.db_session.add(account)
                await self.db_session.flush()

                return account
        except IntegrityError:
            await self.db_session.rollback()
            return None

    async def deleteAccount(self, session_name):
        account = await self.getAccountBySessionName(session_name)
        if account:
            await self.db_session.delete(account)
            await self.db_session.flush()
            return True
        else:
            return False

    async def updateTargetChat(self, session_name, new_target_chat):
        account = await self.getAccountBySessionName(session_name)
        if account:
            account.target_chat = new_target_chat
            await self.db_session.flush()
            return True
        else:
            return False

    async def updateMessage(self, session_name, new_message):
        account = await self.getAccountBySessionName(session_name)
        if account:
            account.message = new_message
            await self.db_session.flush()
            return True
        else:
            return False

    async def addAdvertisingChannel(self, session_name, channel_name):
        account = await self.getAccountBySessionName(session_name)
        if account:
            if account.advertising_channels is None:
                account.advertising_channels = []

            if channel_name not in account.advertising_channels:
                account.advertising_channels.append(channel_name)
                self.db_session.add(account)
                await self.db_session.flush()
                return True

        return False

    async def removeAdvertisingChannel(self, session_name, channel_name):
        account = await self.getAccountBySessionName(session_name)
        if account and account.advertising_channels:
            if channel_name in account.advertising_channels:
                account.advertising_channels.remove(channel_name)
                await self.db_session.flush()
                return True
        return False

    async def getAccountBySessionName(self, session_name):
        result = await self.db_session.execute(
            select(Account).filter(
                Account.session_file_path.ilike(f"%{session_name}.session")
            )
        )
        return result.scalar()
