import asyncio
from datetime import datetime, time, timedelta

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

from app.domain.users import UserUncommited
from app.domain.users import UsersRepository
from app.infrastructure.application import send_report_request, time_difference
from config import SERVER_ID, REPORT_REQUEST_TIME, DAILY_REPORT_TIME, CHANNELS_ROLES_NAMES_DICT

import app.infrastructure.logging.settings as settings

logger = settings.logging.getLogger("discord")

report_request_time = REPORT_REQUEST_TIME + time_difference()
daily_report_time = DAILY_REPORT_TIME + time_difference()


class ReportTasks(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.request_report.start()
        self.request_daily_report.start()

    @staticmethod
    def seconds_until(hours, minutes):
        given_time = time(hours, minutes)
        now = datetime.now()
        future_exec = datetime.combine(now, given_time)
        if (future_exec - now).days < 0:  # If we are past the execution, it will take place tomorrow
            future_exec = datetime.combine(now + timedelta(days=1), given_time)  # days always >= 0

        return (future_exec - now).total_seconds()

    @tasks.loop(hours=24)
    async def request_report(self):
        # Send report request to all users
        await asyncio.sleep(self.seconds_until(hours=report_request_time, minutes=0))
        users = UsersRepository.get_all_users(self.bot)
        async for user in users:
            await send_report_request(user)
        logger.info("Send report request to all users")

    @tasks.loop(hours=24)
    async def request_daily_report(self):
        await asyncio.sleep(self.seconds_until(hours=daily_report_time, minutes=0))
        server = self.bot.get_guild(int(SERVER_ID))

        for channel_name, role_name in CHANNELS_ROLES_NAMES_DICT.items():
            if server:
                channel = discord.utils.get(server.text_channels, name=channel_name)
                content = ''
                now = datetime.now()

                if channel:
                    users_filter = [
                        UserUncommited.model_validate(user)
                        async for user in UsersRepository().filter(department_=role_name)
                    ]
                    if users_filter:
                        for user in users_filter:
                            if (now.replace(hour=report_request_time, minute=0, second=0) <
                                    user.update_date <
                                    now.replace(hour=daily_report_time, minute=0, second=0)):
                                user_info = f"**{user.name}**: {user.report}\n"
                                content = content + user_info
                        if content:
                            await channel.send(content=content)
        logger.info("Send daily report")

    def cog_unload(self):
        self.request_report.cancel()
        self.request_daily_report.cancel()


async def setup_report_tasks(bot):
    await bot.add_cog(ReportTasks(bot))
