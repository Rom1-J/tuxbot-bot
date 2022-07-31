"""
Tags creation view
"""
import discord

from ...models.Tags import TagsModel


class TagCreationModal(discord.ui.Modal):
    """
    Tag creation modal
    """

    title = "Create a tag"

    name = discord.ui.TextInput(
        label="Name", placeholder="Tag name here...", max_length=20
    )

    content = discord.ui.TextInput(
        label="Content",
        style=discord.TextStyle.long,
        placeholder="Tag content here...",
        max_length=1900,
    )

    # =========================================================================
    # =========================================================================

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """Save tag on submit"""

        name = self.name.value.lower()
        content = self.content.value

        if await TagsModel.exists(name=name, guild_id=interaction.guild_id):
            await interaction.response.send_message(
                f"Tag '{name}' already exists.\n\n"
                "Your content: (in case you did not copy it)\n"
                f">>> {discord.utils.escape_markdown(content)}",
                ephemeral=True,
            )
            return

        tag = await TagsModel.create(
            guild_id=interaction.guild_id,
            author_id=interaction.user.id,
            name=name,
            content=discord.utils.escape_mentions(content),
        )

        await interaction.response.send_message(
            f"Tag '{tag.name}' successfully created!", ephemeral=True
        )
