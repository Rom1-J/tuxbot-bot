import logging

from discord.ext import commands

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from tuxbot.core.utils import checks
from tuxbot.core.utils.functions.extra import command_extra, ContextPlus

log = logging.getLogger("tuxbot.cogs.Test")
_ = Translator("Test", __file__)


class Test(commands.Cog):
    def __init__(self, bot: Tux, version_info):
        self.bot = bot
        self.version_info = version_info

    # =========================================================================
    # =========================================================================

    @command_extra(name="crash", deletable=True)
    @checks.is_owner()
    async def _crash(self, ctx: ContextPlus, crash_type: str):
        if crash_type == "ZeroDivisionError":
            await ctx.send(str(5 / 0))
        elif crash_type == "TypeError":
            # noinspection PyTypeChecker
            await ctx.send(str(int([])))  # type: ignore
        elif crash_type == "IndexError":
            await ctx.send(str([0][5]))

    # =========================================================================
