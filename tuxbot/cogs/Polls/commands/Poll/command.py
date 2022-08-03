"""
tuxbot.cogs.Polls.commands.poll.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage polls
"""
import discord
from discord import app_commands
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


@app_commands.guild_only()
class PollCommand(commands.GroupCog, name="poll"):  # type: ignore
    """Manage polls"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        super().__init__()

    # =========================================================================
    # =========================================================================

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        """Whenever this command raise an error"""

        if isinstance(error, app_commands.CheckFailure):
            return

        await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )

        self.bot.logger.error(error)

    # =========================================================================
    # =========================================================================

    @app_commands.command(name="create", description="Create a poll")
    @app_commands.describe(name="Poll name")
    async def _poll_create(
        self, interaction: discord.Interaction, name: str
    ) -> None:
        await interaction.response.send_message("dza", ephemeral=True)
