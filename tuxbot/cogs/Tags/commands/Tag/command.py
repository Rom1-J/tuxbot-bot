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


class TagCommand(commands.Cog, app_commands.Group, name="tag"):
    """Manage tags"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot
        super().__init__()

    # =========================================================================
    # =========================================================================

    @app_commands.command(name="get", description="Print a tag")
    @app_commands.describe(name="Tag name")
    async def _tag(self, interaction: discord.Interaction, name: str) -> None:
        await interaction.response.send_message(name)

    @app_commands.command(name="create", description="Create a tag")
    async def _tag_create(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(TagCreationModal())
