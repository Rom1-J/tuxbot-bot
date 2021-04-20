import logging
from discord.ext import commands

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)
from tuxbot.core.utils import checks
from tuxbot.core.utils.functions.extra import command_extra, ContextPlus

log = logging.getLogger("tuxbot.cogs.Dev")
_ = Translator("Dev", __file__)


class Dev(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot

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
