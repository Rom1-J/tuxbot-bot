import logging

from discord.ext import commands
from jishaku.models import copy_context_with

from tuxbot.core.utils import checks
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from tuxbot.core.utils.functions.extra import (
    command_extra,
    ContextPlus,
)

log = logging.getLogger("tuxbot.cogs.Admin")
_ = Translator("Admin", __file__)


class Admin(commands.Cog):
    def __init__(self, bot: Tux, version_info):
        self.bot = bot
        self.version_info = version_info

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

    @command_extra(name="update", deletable=False)
    @checks.is_owner()
    async def _update(self, ctx: ContextPlus):
        sh = "jsk sh"

        git = f"{sh} git pull"
        update = f"{sh} make update"

        git_command_ctx = await copy_context_with(
            ctx, content=ctx.prefix + git
        )
        update_command_ctx = await copy_context_with(
            ctx, content=ctx.prefix + update
        )

        await git_command_ctx.command.invoke(git_command_ctx)
        await update_command_ctx.command.invoke(update_command_ctx)

        await self._restart(ctx)
