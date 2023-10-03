import asyncio

from app.infrastructure.database import Base
from app.infrastructure.database.session import engine


async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(prepare_database())
