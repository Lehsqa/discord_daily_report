from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from discord.colour import Colour

import app.infrastructure.logging.settings as settings
from config import SERVER_ID, CHANNELS_ROLES_NAMES_DICT, CATEGORY_NAME

logger = settings.logging.getLogger("discord")


class ChannelsRolesCommands(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command('create_channels_roles')
    async def create_channels_roles(self, ctx):
        try:
            server = self.bot.get_guild(int(SERVER_ID))

            category = get(server.categories, name=CATEGORY_NAME)
            if not category:
                category = await server.create_category(CATEGORY_NAME)

            for channel_name in CHANNELS_ROLES_NAMES_DICT.keys():
                if not get(server.text_channels, name=channel_name):
                    await server.create_text_channel(channel_name, category=category)

            for role_name in CHANNELS_ROLES_NAMES_DICT.values():
                if not get(server.roles, name=role_name):
                    await server.create_role(name=role_name, colour=Colour.default())
            logger.info(f'Creating channels and roles: success')
        except Exception as e:
            logger.info(f'Error in creating channels and roles: {e}')


async def setup_channels_roles_commands(bot):
    await bot.add_cog(ChannelsRolesCommands(bot))
