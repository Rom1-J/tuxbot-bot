"""Tags edition view."""
import typing

import discord

from tuxbot.cogs.Tags.commands.Tag.models.tags import TagsModel


class TagEditionModal(discord.ui.Modal):
    """Tag edition modal."""

    title = "Edit a tag"

    def __init__(self: typing.Self, tag: TagsModel) -> None:
        super().__init__()

        self.__tag = tag

        self.content: discord.ui.TextInput[
            TagEditionModal
        ] = discord.ui.TextInput(
            label="Content",
            style=discord.TextStyle.long,
            placeholder="Tag content here...",
            max_length=1900,
            default=self.__tag.content,
        )
        self.add_item(self.content)

    # =========================================================================
    # =========================================================================

    async def on_submit(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        """Save tag on submit."""
        self.__tag.content = discord.utils.escape_mentions(
            self.content.value or ""
        )
        await self.__tag.save()

        await interaction.response.send_message(
            f"Tag '{self.__tag.name}' successfully edited!", ephemeral=True
        )
