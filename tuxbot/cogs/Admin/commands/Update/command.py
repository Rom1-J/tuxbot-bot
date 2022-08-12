"""
tuxbot.cogs.Admin.commands.Update.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command to update Tuxbot
"""

from discord.ext import commands
from jishaku.models import copy_context_with

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot


class UpdateCommand(commands.Cog):
    """Update tuxbot"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command("update")
    async def _update(self, ctx: commands.Context[TuxbotABC]) -> None:
        sh = "jsk sh"
        prefix = ctx.prefix or (
            f"<@{ctx.bot.user.id}>" if ctx.bot.user else ""
        )

        git = f"{sh} git pull"
        update = f"{sh} make update"

        git_command_ctx = await copy_context_with(ctx, content=prefix + git)
        update_command_ctx = await copy_context_with(
            ctx, content=prefix + update
        )

        if git_command_ctx.command and update_command_ctx.command:
            await git_command_ctx.command.invoke(git_command_ctx)
            await update_command_ctx.command.invoke(update_command_ctx)

            if command := self.bot.get_command("restart"):
                await command(ctx)
