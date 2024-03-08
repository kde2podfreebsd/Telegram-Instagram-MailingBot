from alembic import command
from alembic.config import Config
import asyncio

async def asyncInitializeDatabase():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, initializeDatabase)
    return result

def initializeDatabase():
    alembic_cfg = Config("App/Database/alembic.ini")
    
    command.revision(
        config=alembic_cfg, 
        message="Migrations has been initialized successfully", 
        autogenerate=True
    )

    command.upgrade(
        alembic_cfg, 
        "head"
    )

