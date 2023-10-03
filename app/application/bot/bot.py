import asyncio
from datetime import datetime, time, timedelta

import pytz
from discord.ext import commands

from app.application.commands import setup_channels_roles_commands
from app.application.tasks import setup_report_tasks
from app.domain.users import UserUncommited
from app.domain.users import UsersRepository
from app.infrastructure.application import reply_request, get_department, time_difference
from app.infrastructure.errors import DatabaseError
from config import TIME_ZONE, REPORT_REQUEST_TIME, DAILY_REPORT_TIME, SERVER_ID

import app.infrastructure.logging.settings as settings

logger = settings.logging.getLogger("discord")


class Bot(commands.Bot):
    def __init__(self, command_prefix, intents, token):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.token = token

    @staticmethod
    def time_check():
        return (time(REPORT_REQUEST_TIME, 0, 0) <
                datetime.now(pytz.timezone(TIME_ZONE)).time() <
                time(DAILY_REPORT_TIME, 0, 0))

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        await self.setup_tasks()

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        await self.process_commands(message)

        if not message.content.startswith('!'):
            if self.time_check():
                try:
                    server = self.get_guild(int(SERVER_ID))
                    department = get_department(server, message)
                    await UsersRepository().create_or_update(UserUncommited(name=message.author.name,
                                                                            department=department,
                                                                            report=message.content,
                                                                            update_date=datetime.now() + timedelta(
                                                                                hours=time_difference())
                                                                            ))
                    await reply_request(message, text="Your request was saved")
                    logger.info(f'User "{message.author.name}": send his report')
                except DatabaseError:
                    await reply_request(message, text="There are some problem with saving your request")
                    logger.info(f'User "{message.author.name}": get error with database')
            else:
                await reply_request(message, text=f"Please, sent report after {REPORT_REQUEST_TIME}:00")
                logger.info(f'User "{message.author.name}": try to send report early than {REPORT_REQUEST_TIME}:00')

    async def setup_tasks(self):
        await setup_report_tasks(self)

    async def setup_commands(self):
        await setup_channels_roles_commands(self)

    def run_bot(self):
        asyncio.run(self.setup_commands())
        self.run(self.token)
