import logging

from discord.ext import commands

from tuxbot.core import checks
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator

log = logging.getLogger("tuxbot.cogs.anti_raid")
T_ = Translator("AntiRaid", __file__)


class AntiRaid(commands.Cog, name="AntiRaid"):
    def __init__(self, bot: Tux):
        self.bot = bot

    @commands.group(
        name="anti_raid",
        alias=["anti-raid", "raid_protect", "raid-protect", "no_raid", "no-raid"],
    )
    @commands.guild_only()
    @checks.is_admin()
    async def _anti_raid(self, ctx: commands.Context):
        pass
