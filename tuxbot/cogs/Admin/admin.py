import logging

from discord.ext import commands

from tuxbot.core.utils import checks
from tuxbot.core.bot import Tux
from tuxbot.core.config import set_for_key
from tuxbot.core.config import Config
from tuxbot.core.i18n import (
    Translator,
)
from tuxbot.core.utils.functions.extra import (
    command_extra,
    ContextPlus,
)

log = logging.getLogger("tuxbot.cogs.Admin")
_ = Translator("Admin", __file__)


class Admin(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot

    async def _save_lang(self, ctx: ContextPlus, lang: str):
        set_for_key(
            self.bot.config.Servers, ctx.guild.id, Config.Server, locale=lang
        )

    # =========================================================================
    # =========================================================================

    @command_extra(name="quit", aliases=["shutdown"], deletable=False)
    @checks.is_owner()
    async def _quit(self, ctx: ContextPlus):
        await ctx.send("*quit...*")
        await self.bot.shutdown()

    @command_extra(name="restart", deletable=False)
    @checks.is_owner()
    async def _restart(self, ctx: ContextPlus):
        await ctx.send("*restart...*")
        await self.bot.shutdown(restart=True)
