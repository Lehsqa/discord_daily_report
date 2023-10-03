from sqlalchemy import Result
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.errors.base import DatabaseError

from config import DATABASE_URL

engine: AsyncEngine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False
)


class Session:
    # All sqlalchemy errors that can be raised
    _ERRORS = (IntegrityError, PendingRollbackError)

    def __init__(self) -> None:
        self._async_session = async_session

    async def execute(self, query) -> Result:
        try:
            async with self._async_session() as session:
                async with session.begin():
                    result = await session.execute(query)
            return result
        except self._ERRORS:
            raise DatabaseError

    async def save(self, schema):
        try:
            async with self._async_session() as session:
                async with session.begin():
                    session.add(schema)
                    await session.flush()
                    await session.refresh(schema)
                    await session.commit()
        except self._ERRORS:
            raise DatabaseError
