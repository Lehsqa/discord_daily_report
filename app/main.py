import discord

from app.application.bot import Bot
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True


if __name__ == "__main__":
    bot = Bot(command_prefix='!', intents=intents, token=BOT_TOKEN)
    bot.run_bot()
