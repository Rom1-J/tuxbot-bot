"""
tuxbot.cogs.Tags.commands.Tag.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage tags
"""
from typing import Dict, List, Optional, Union

import discord
from discord import app_commands
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .models.Tags import TagsModel
from .ui.modals.TagCreationModal import TagCreationModal
from .ui.modals.TagEditionModal import TagEditionModal
from .ui.paginator import TagPages


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

    @staticmethod
    async def __get_tags(
            guild_id: int,
            member_id: Optional[int] = None,
            query: Optional[str] = None
    ) -> Optional[List[TagsModel]]:
        kwargs: Dict[str, Union[str, int]] = {
            "guild_id": guild_id
        }

        if member_id is not None:
            kwargs["author_id"] = member_id

        if query is not None:
            kwargs["name__icontains"] = query

        return await TagsModel.filter(**kwargs).all().order_by("-uses")

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

    @app_commands.command(name="raw", description="Print a tag as raw")
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

    # =========================================================================

    @app_commands.command(name="info", description="Show tag's info")
    @app_commands.describe(name="Tag name")
    async def _tag_info(
            self,
            interaction: discord.Interaction,
            name: str
    ) -> None:
        if tag := await self.__get_tag(interaction.guild_id, name):
            e = discord.Embed(color=discord.Colour.blue())

            user = await self.bot.fetch_member_or_none(
                interaction.guild, tag.author_id
            ) or await self.bot.fetch_user_or_none(tag.author_id)

            e.title = tag.name
            e.description = tag.content
            e.timestamp = tag.created_at

            if user:
                e.set_author(name=user, icon_url=user.display_avatar.url)

            e.set_footer(text=f"Uses: {tag.uses}")

            await interaction.response.send_message(embed=e)
            return

        await interaction.response.send_message(
            f"Tag '{name}' not found...",
            ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="list", description="List all tags of member")
    @app_commands.describe(member="Member to search")
    async def _tag_list(
            self,
            interaction: discord.Interaction,
            member: Optional[discord.Member] = None
    ) -> None:
        member = member or interaction.user

        tags = await self.__get_tags(
            guild_id=interaction.guild_id, member_id=member.id
        )

        if tags:
            p = TagPages(tags, ctx=interaction)
            await p.start()
            return

        await interaction.response.send_message(
            f"No tags found for {member}...",
            ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="all", description="List all tags")
    async def _tag_all(self, interaction: discord.Interaction) -> None:
        tags = await self.__get_tags(guild_id=interaction.guild_id)

        if tags:
            p = TagPages(tags, ctx=interaction)
            await p.start()
            return

        await interaction.response.send_message(
            "No tags found...",
            ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="claim", description="Claim orphelin tag")
    @app_commands.describe(name="Tag name")
    async def _tag_claim(
            self,
            interaction: discord.Interaction,
            name: str
    ) -> None:
        if tag := await self.__get_tag(interaction.guild_id, name):
            if await self.bot.fetch_member_or_none(
                    interaction.guild, tag.author_id
            ) is not None:
                await interaction.response.send_message(
                    "Tag owner is on this server.",
                    ephemeral=True
                )
                return

            tag.author_id = interaction.user.id
            await tag.save()

            await interaction.response.send_message(
                "This tag is now owned by you.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"Tag '{name}' not found...",
            ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="search", description="Search for tags")
    @app_commands.describe(query="Query")
    async def _tag_search(
            self,
            interaction: discord.Interaction,
            query: str
    ) -> None:
        tags = await self.__get_tags(
            guild_id=interaction.guild_id, query=query
        )

        if tags:
            p = TagPages(tags, ctx=interaction)
            await p.start()
            return

        await interaction.response.send_message(
            "No tags found...",
            ephemeral=True
        )
