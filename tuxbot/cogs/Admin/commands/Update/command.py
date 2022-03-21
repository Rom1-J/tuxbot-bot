"""
tuxbot.cogs.Admin.commands.Update.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command to update Tuxbot
"""

from discord.ext import commands
from jishaku.models import copy_context_with

from tuxbot.core.Tuxbot import Tuxbot


class UpdateCommand(commands.Cog):
    """Update tuxbot"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command("update")
    async def _update(self, ctx: commands.Context):
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

        await self.bot.get_command("restart")(ctx)
