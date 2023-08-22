"""
tuxbot.cogs.Tags.commands.Tag.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Manage tags
"""
import json
import typing

import discord
from discord import app_commands
from discord.ext import commands

from tuxbot.core.tuxbot import Tuxbot

from .models.tags import TagsModel
from .ui.modals.tag_creation_modal import TagCreationModal
from .ui.modals.tag_edition_modal import TagEditionModal
from .ui.paginator import TagPages


@app_commands.guild_only()
class TagCommand(commands.GroupCog, name="tag"):  # type: ignore[call-arg]
    """Manage tags."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

        super().__init__()

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __get_tag(guild_id: int, name: str) -> TagsModel | None:
        tags: TagsModel | None = await TagsModel.get_or_none(
            guild_id=guild_id, name=name.lower()
        )
        return tags

    # =========================================================================

    @staticmethod
    async def __get_tags(
        guild_id: int, member_id: int | None = None, query: str | None = None
    ) -> list[TagsModel] | None:
        kwargs: dict[str, str | int] = {"guild_id": guild_id}

        if member_id is not None:
            kwargs["author_id"] = member_id

        if query is not None:
            kwargs["name__icontains"] = query

        tags: list[TagsModel] | None = (
            await TagsModel.filter(**kwargs).limit(25).order_by("-uses")
        )

        return tags

    # =========================================================================

    async def __tag_get_autocomplete(
        self: typing.Self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        if not interaction.guild:
            msg = ""
            raise commands.GuildNotFound(msg)

        cache_key = self.bot.utils.gen_key(interaction.guild.id, current)

        if data := await self.bot.redis.get(cache_key):
            tags = json.loads(data) or []
        else:
            tags = [
                t.name
                for t in (
                    await self.__get_tags(interaction.guild.id, query=current)
                    or []
                )
            ]

            await self.bot.redis.set(cache_key, json.dumps(tags), ex=3600)

        return [
            app_commands.Choice(name=tag, value=tag)
            for tag in tags
            if current.lower() in tag.lower()
        ]

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def interaction_check(interaction: discord.Interaction) -> bool:
        """Run checks before processing command."""
        if interaction.guild is None:
            await interaction.response.send_message(
                "This command can only be used in a guild"
            )
            return False

        return True

    # =========================================================================

    async def on_error(
        self: typing.Self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        """Whenever this command raise an error."""
        if isinstance(error, app_commands.CheckFailure):
            return

        await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )

        self.bot.logger.exception(error)

    # =========================================================================
    # =========================================================================

    # noinspection PyTypeChecker
    @app_commands.command(name="get", description="Print a tag")
    @app_commands.describe(name="Tag name")
    @app_commands.autocomplete(name=__tag_get_autocomplete)
    async def _tag_get(
        self: typing.Self, interaction: discord.Interaction, name: str
    ) -> None:
        if not interaction.guild:
            msg = ""
            raise commands.GuildNotFound(msg)

        if tag := await self.__get_tag(interaction.guild.id, name):
            await interaction.response.send_message(tag.content)

            tag.uses += 1
            await tag.save()

            return

        await interaction.response.send_message(
            f"Tag '{name}' not found...", ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="raw", description="Print a tag as raw")
    @app_commands.describe(name="Tag name")
    async def _tag_raw(
        self: typing.Self, interaction: discord.Interaction, name: str
    ) -> None:
        if not interaction.guild:
            msg = ""
            raise commands.GuildNotFound(msg)

        if tag := await self.__get_tag(interaction.guild.id, name):
            await interaction.response.send_message(
                discord.utils.escape_markdown(tag.content)
            )

            tag.uses += 1
            await tag.save()

            return

        await interaction.response.send_message(
            f"Tag '{name}' not found...", ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="create", description="Create a tag")
    async def _tag_create(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        await interaction.response.send_modal(TagCreationModal())

    # =========================================================================

    @app_commands.command(name="delete", description="Delete a tag")
    @app_commands.describe(name="Tag name")
    async def _tag_delete(
        self: typing.Self, interaction: discord.Interaction, name: str
    ) -> None:
        if not interaction.guild:
            msg = ""
            raise commands.GuildNotFound(msg)

        if tag := await self.__get_tag(interaction.guild.id, name):
            if tag.author_id == interaction.user.id:
                await tag.delete()

                await interaction.response.send_message(
                    f"Tag '{name}' deleted successfully!", ephemeral=True
                )
                return

            await interaction.response.send_message(
                f"You must be the owner of '{name}' to delete it...",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"Tag '{name}' not found...", ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="edit", description="Edit a tag")
    @app_commands.describe(name="Tag name")
    async def _tag_edit(
        self: typing.Self, interaction: discord.Interaction, name: str
    ) -> None:
        if not interaction.guild:
            msg = ""
            raise commands.GuildNotFound(msg)

        if tag := await self.__get_tag(interaction.guild.id, name):
            if tag.author_id == interaction.user.id:
                await interaction.response.send_modal(TagEditionModal(tag))

                return

            await interaction.response.send_message(
                f"You must be the owner of '{name}' to edit it...",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"Tag '{name}' not found...", ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="info", description="Show tag's info")
    @app_commands.describe(name="Tag name")
    async def _tag_info(
        self: typing.Self, interaction: discord.Interaction, name: str
    ) -> None:
        if not interaction.guild:
            msg = ""
            raise commands.GuildNotFound(msg)

        if tag := await self.__get_tag(interaction.guild.id, name):
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
            f"Tag '{name}' not found...", ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="list", description="List all tags of member")
    @app_commands.describe(member="Member to search")
    async def _tag_list(
        self: typing.Self,
        interaction: discord.Interaction,
        member: discord.Member | None = None,
    ) -> None:
        if not interaction.guild:
            msg = ""
            raise commands.GuildNotFound(msg)

        _member = member or interaction.user

        if not _member:
            msg = ""
            raise commands.MemberNotFound(msg)

        tags = await self.__get_tags(
            guild_id=interaction.guild.id, member_id=_member.id
        )

        if tags:
            p = TagPages(tags, ctx=interaction)
            await p.start()
            return

        await interaction.response.send_message(
            f"No tags found for {_member}...", ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="all", description="List all tags")
    async def _tag_all(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        if not interaction.guild:
            msg = ""
            raise commands.GuildNotFound(msg)

        tags = await self.__get_tags(guild_id=interaction.guild.id)

        if tags:
            p = TagPages(tags, ctx=interaction)
            await p.start()
            return

        await interaction.response.send_message(
            "No tags found...", ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="claim", description="Claim orphelin tag")
    @app_commands.describe(name="Tag name")
    async def _tag_claim(
        self: typing.Self, interaction: discord.Interaction, name: str
    ) -> None:
        if not interaction.guild:
            msg = ""
            raise commands.GuildNotFound(msg)

        if tag := await self.__get_tag(interaction.guild.id, name):
            if (
                await self.bot.fetch_member_or_none(
                    interaction.guild, tag.author_id
                )
                is not None
            ):
                await interaction.response.send_message(
                    "Tag owner is on this server.", ephemeral=True
                )
                return

            tag.author_id = interaction.user.id
            await tag.save()

            await interaction.response.send_message(
                "This tag is now owned by you.", ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"Tag '{name}' not found...", ephemeral=True
        )

    # =========================================================================

    @app_commands.command(name="search", description="Search for tags")
    @app_commands.describe(query="Query")
    async def _tag_search(
        self: typing.Self, interaction: discord.Interaction, query: str
    ) -> None:
        if not interaction.guild:
            msg = ""
            raise commands.GuildNotFound(msg)

        tags = await self.__get_tags(
            guild_id=interaction.guild.id, query=query
        )

        if tags:
            p = TagPages(tags, ctx=interaction)
            await p.start()
            return

        await interaction.response.send_message(
            "No tags found...", ephemeral=True
        )
