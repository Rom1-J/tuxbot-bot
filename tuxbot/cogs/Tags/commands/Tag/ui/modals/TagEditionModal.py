"""
Tags edition view
"""
import discord

from ...models.Tags import TagsModel


class TagEditionModal(discord.ui.Modal):
    """
    Tag edition modal
    """

    title = "Edit a tag"

    def __init__(self, tag: TagsModel):
        super().__init__()

        self.__tag = tag

        self.content = discord.ui.TextInput(
            label="Content",
            style=discord.TextStyle.long,
            placeholder="Tag content here...",
            max_length=1900,
            default=self.__tag.content,
        )
        self.add_item(self.content)

    # =========================================================================
    # =========================================================================

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """Save tag on submit"""

        self.__tag.content = discord.utils.escape_mentions(self.content.value)
        await self.__tag.save()

        await interaction.response.send_message(
            f"Tag '{self.__tag.name}' successfully edited!", ephemeral=True
        )
