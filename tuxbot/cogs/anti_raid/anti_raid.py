import logging

from discord.ext import commands

from tuxbot.core import checks
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator

log = logging.getLogger("tuxbot.cogs.admin")
T_ = Translator("Admin", __file__)


class Admin(commands.Cog, name="Admin"):
    def __init__(self, bot: Tux):
        self.bot = bot

    @commands.group(
        name="anti_raid",
        alias=["anti-raid", "raid_protect", "raid-protect", "no_raid", "no-raid"],
    )
    @commands.guild_only()
    @checks.is_admin()
    async def _warn(self, ctx: commands.Context):
        pass
