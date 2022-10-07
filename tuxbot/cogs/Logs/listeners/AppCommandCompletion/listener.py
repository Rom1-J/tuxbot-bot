"""
tuxbot.cogs.Logs.listeners.AppCommandCompletion.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever an app command is completed
"""
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class AppCommandCompletion(commands.Cog):
    """Listener whenever an app command is completed"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_app_command_completion")
    async def _on_app_command_completion(
        self,
        interaction: discord.Interaction,
        command: discord.app_commands.Command  # type: ignore[type-arg]
        | discord.app_commands.ContextMenu,
    ) -> None:
        self.bot.logger.info(
            "[AppCommandCompletion] App Command '%s' completed.",
            command.qualified_name,
        )

        self.bot.statsd.increment(
            "command_success",
            value=1,
            tags=[f"command:{command.qualified_name}"],
        )
