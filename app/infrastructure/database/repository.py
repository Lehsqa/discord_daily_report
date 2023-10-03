from typing import Any, AsyncGenerator, Generic, Type

from sqlalchemy import Result, select, update

from app.infrastructure.database.session import Session
from app.infrastructure.database.tables import ConcreteTable
from app.infrastructure.errors.base import (
    NotFoundError,
    UnprocessableError,
)


class BaseRepository(Session, Generic[ConcreteTable]):  # type: ignore
    """This class implements the base interface for working with database
    # and makes it easier to work with type annotations.
    """

    schema_class: Type[ConcreteTable]

    def __init__(self) -> None:
        super().__init__()

        if not self.schema_class:
            raise UnprocessableError(
                message=(
                    "Can not initiate the class without schema_class attribute"
                )
            )

    async def _filter(self, key: str, value: Any) -> AsyncGenerator[ConcreteTable, None]:
        query = select(
            self.schema_class
        ).where(
            getattr(self.schema_class, key) == value
        )
        result: Result = await self.execute(query)
        schemas = result.scalars().all()

        for schema in schemas:
            yield schema

    async def _get(self, key: str, value: Any) -> ConcreteTable:
        query = select(
            self.schema_class
        ).where(
            getattr(self.schema_class, key) == value
        )
        result: Result = await self.execute(query)

        if not (_result := result.scalars().one_or_none()):
            raise NotFoundError

        return _result

    async def _save(self, payload: dict[str, Any]) -> ConcreteTable:
        schema = self.schema_class(**payload)
        await self.save(schema)
        return schema

    async def _update(self, key: str, value: Any, fields: list[str], data):
        query = update(
            self.schema_class
        ).where(
            getattr(self.schema_class, key) == value
        ).values(
            {getattr(self.schema_class, field): getattr(data, field) for field in fields}
        )
        result: Result = await self.execute(query)

        return result
