from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import and_

from App.Database.Models.Models import ProxyAddress
from App.Logger import ApplicationLogger

logger = ApplicationLogger()


class ProxyAddressDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def createProxyAddress(self, address, account_inst_id):
        try:
            proxy = ProxyAddress(
                address=address, 
                account_inst_id=account_inst_id
            )
            self.db_session.add(proxy)
            await self.db_session.flush()
            return proxy
        except IntegrityError:
            await self.db_session.rollback()
            logger.log_warning("IntegrityError, db rollback")
            return None

    async def deleteProxyAddress(self, address, account_inst_id):
        proxy = await self.getProxyAddress(
            address=address, 
            account_inst_id=account_inst_id
        )
        if proxy:
            await self.db_session.delete(proxy)
            await self.db_session.flush()
            logger.log_info(f"ProxyAddress {address} has been removed from the data base")
            return True
        else:
            logger.log_error("ProxyAddress doesn't exist in database")
            return False

    async def getProxyAddress(self, address, account_inst_id):
        query = select(ProxyAddress).where(ProxyAddress.address == address).where(ProxyAddress.account_inst_id == account_inst_id)
        result = await self.db_session.execute(query)
        return result.scalar()
    
    async def getProxyAddressById(self, account_inst_id):
        query = select(ProxyAddress).filter(ProxyAddress.account_inst_id == account_inst_id)
        result = await self.db_session.execute(query)
        return [proxy.address for proxy in result.scalars()]
    