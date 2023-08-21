"""
tuxbot.cogs.Logs.listeners.CommandCompletion.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Listener whenever command is completed
"""
import typing
from datetime import UTC, datetime

from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.core.tuxbot import Tuxbot


class CommandCompletion(commands.Cog):
    """Listener whenever command is completed."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_command_completion")
    async def _on_command_completion(
        self: typing.Self, ctx: commands.Context[TuxbotABC]
    ) -> None:
        if not ctx.command:
            return

        command = ctx.command.name

        if parent_name := ctx.command.full_parent_name:
            command = f"{parent_name} {ctx.command.name}"

        delta = datetime.now(tz=UTC) - ctx.message.created_at

        self.bot.logger.info(
            "[CommandCompletion] Command '%s' completed in %d ms.",
            command,
            delta.total_seconds() * 1000,
        )

        self.bot.statsd.increment(
            "command_success", value=1, tags=[f"command:{command}"]
        )
