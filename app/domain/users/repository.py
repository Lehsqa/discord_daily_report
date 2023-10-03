from discord.ext.commands import Bot
from discord.types.member import Member

from typing import AsyncGenerator

from app.infrastructure.database import BaseRepository, UsersTable

from app.domain.users import UserUncommited
from app.infrastructure.errors import NotFoundError
from config import SERVER_ID


class UsersRepository(BaseRepository[UsersTable]):
    schema_class = UsersTable

    @staticmethod
    async def get_all_users(bot: Bot) -> AsyncGenerator[Member, None]:
        server = bot.get_guild(int(SERVER_ID))
        for user in server.members:
            if not user.bot:
                yield user

    async def create_or_update(self, schema: UserUncommited) -> str:
        try:
            await self._get(key="name", value=schema.name)
            await self._update(key="name", value=schema.name, fields=["department", "report", "update_date"],
                               data=schema)
            return "Successfully updated"
        except NotFoundError:
            await self._save(schema.model_dump())
            return "Successfully created"
        finally:
            return "Data base error: cant create or update"

    async def filter(self, department_: str) -> AsyncGenerator[UserUncommited, None]:
        async for instance in self._filter(key="department", value=department_):
            yield UserUncommited.model_validate(instance)
