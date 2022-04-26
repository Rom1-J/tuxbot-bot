"""
tuxbot.cogs.Tags.commands.Tag.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage tags
"""
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .models.Tags import TagsModel
from .ui.modals.TagCreationModal import TagCreationModal
from .ui.modals.TagEditionModal import TagEditionModal


class TagCommand(commands.Cog, app_commands.Group, name="tag"):  # type: ignore
    """Manage tags"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        super().__init__()

    @staticmethod
    async def __get_tag(guild_id: int, name: str) -> Optional[TagsModel]:
        return await TagsModel.get_or_none(
            guild_id=guild_id, name=name.lower()
        )

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
        if tag := await self.__get_tag(interaction.guild_id, name):
            await interaction.response.send_message(tag.content)

            tag.uses += 1
            await tag.save()

            return

        await interaction.response.send_message(
            f"Tag '{name}' not found...",
            ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="raw", description="Print a tag as aaw")
    @app_commands.describe(name="Tag name")
    async def _tag_raw(
            self, interaction: discord.Interaction, name: str
    ) -> None:
        if tag := await self.__get_tag(interaction.guild_id, name):
            await interaction.response.send_message(
                discord.utils.escape_markdown(tag.content)
            )

            tag.uses += 1
            await tag.save()

            return

        await interaction.response.send_message(
            f"Tag '{name}' not found...",
            ephemeral=True
        )

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
        if tag := await self.__get_tag(interaction.guild_id, name):
            if tag.author_id == interaction.user.id:
                await tag.delete()

                await interaction.response.send_message(
                    f"Tag '{name}' deleted successfully!",
                    ephemeral=True
                )
                return

            await interaction.response.send_message(
                f"You must be the owner of '{name}' to delete it...",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"Tag '{name}' not found...",
            ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="edit", description="Edit a tag")
    @app_commands.describe(name="Tag name")
    async def _tag_edit(
            self, interaction: discord.Interaction, name: str
    ) -> None:
        if tag := await self.__get_tag(interaction.guild_id, name):
            if tag.author_id == interaction.user.id:
                await interaction.response.send_modal(TagEditionModal(tag))

                return

            await interaction.response.send_message(
                f"You must be the owner of '{name}' to edit it...",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"Tag '{name}' not found...",
            ephemeral=True
        )
