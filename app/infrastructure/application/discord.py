import time
from datetime import datetime

import pytz
from discord.errors import Forbidden
from discord.utils import get

from config import TIME_ZONE, CHANNELS_ROLES_NAMES_DICT


async def send_report_request(user):
    try:
        await user.send("Please submit your daily report.")
    except Forbidden:
        print(f"Failed to send report request to {user.name} ({user.id})")


async def reply_request(message, text: str):
    try:
        await message.reply(text, mention_author=True)
    except Forbidden:
        print(f"Failed to reply request to {message.author.name} ({message.author.id})")


def get_department(server, message):
    departament = 'N/A'
    member = get(server.members, id=int(message.author.id))

    if member:
        for role in member.roles:
            if role.name in CHANNELS_ROLES_NAMES_DICT.values():
                departament = str(role.name)
    return departament


def time_difference():
    local_time = datetime.now()
    local_time_unix = time.mktime(local_time.timetuple())
    another_time = local_time.astimezone(pytz.timezone(TIME_ZONE)).replace(tzinfo=None)
    another_time_unix = time.mktime(another_time.timetuple())
    diff = another_time_unix - local_time_unix
    return int(diff / 3600)

