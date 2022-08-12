"""
tuxbot.cogs.Logs.listeners.CommandCompletion.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever command is completed
"""
from datetime import datetime, timezone

from tuxbot.abc.TuxbotABC import TuxbotABC
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class CommandCompletion(commands.Cog):
    """Listener whenever command is completed"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_command_completion")
    async def _on_command_completion(
        self, ctx: commands.Context[TuxbotABC]
    ) -> None:
        if not ctx.command:
            return

        command = ctx.command.name

        if parent_name := ctx.command.full_parent_name:
            command = f"{parent_name} {ctx.command.name}"

        delta = datetime.now(tz=timezone.utc) - ctx.message.created_at

        self.bot.logger.info(
            "[CommandCompletion] Command '%s' completed in %d ms.",
            command,
            delta.total_seconds() * 1000,
        )

        self.bot.statsd.increment(
            "command_success", value=1, tags=[f"command:{command}"]
        )
