"""
tuxbot.cogs.Tags.commands.Tag.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage tags
"""
import discord
from discord import app_commands
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .ui.modal import TagCreationModal


class TagCommand(commands.Cog, app_commands.Group, name="tag"):  # type: ignore
    """Manage tags"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        super().__init__()

    # =========================================================================
    # =========================================================================

    async def interaction_check(
            self, interaction: discord.Interaction
    ) -> bool:
        """Run checks before processing command"""

        if interaction.guild is None:
            await interaction.response.send_message(
                "This command can only be used in a guild"
            )
            return False

        return True

    # =========================================================================

    async def on_error(
            self,
            interaction: discord.Interaction,
            error: app_commands.AppCommandError
    ) -> None:
        """Whenever this command raise an error"""

        if isinstance(error, app_commands.CheckFailure):
            return

        await interaction.response.send_message(
            "Oops! Something went wrong.",
            ephemeral=True
        )

        self.bot.logger.error(error)

    # =========================================================================
    # =========================================================================

    @app_commands.command(name="get", description="Print a tag")
    @app_commands.describe(name="Tag name")
    async def _tag_get(
            self, interaction: discord.Interaction, name: str
    ) -> None:
        await interaction.response.send_message(f"Show {name}")

    # =========================================================================

    @app_commands.command(name="raw", description="Print a tag as aaw")
    @app_commands.describe(name="Tag name")
    async def _tag_raw(
            self, interaction: discord.Interaction, name: str
    ) -> None:
        await interaction.response.send_message(f"Raw {name}")

    # =========================================================================

    @app_commands.command(name="create", description="Create a tag")
    async def _tag_create(
            self, interaction: discord.Interaction
    ) -> None:
        await interaction.response.send_modal(TagCreationModal())

    # =========================================================================

    @app_commands.command(name="delete", description="Delete a tag")
    @app_commands.describe(name="Tag name")
    async def _tag_delete(
            self, interaction: discord.Interaction, name: str
    ) -> None:
        await interaction.response.send_message(f"Delete {name}")
