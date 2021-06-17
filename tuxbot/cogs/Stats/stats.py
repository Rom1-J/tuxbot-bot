import logging
from discord.ext import commands

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from tuxbot.core.utils.functions.extra import command_extra, ContextPlus

log = logging.getLogger("tuxbot.cogs.Stats")
_ = Translator("Stats", __file__)


class Stats(commands.Cog):
    def __init__(self, bot: Tux, version_info):
        self.bot = bot
        self.version_info = version_info

    # =========================================================================
    # =========================================================================

    @command_extra(name="to_replace", deletable=True)
    async def _to_replace(self, ctx: ContextPlus):
        __ = ctx

    # =========================================================================
