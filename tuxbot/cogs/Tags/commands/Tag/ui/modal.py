"""
Tags creation view
"""
import discord


class TagCreationModal(discord.ui.Modal):
    """
    Tag creation modal
    """

    title = "Create tag"

    name = discord.ui.TextInput(
        label="Name",
        placeholder="Tag name here...",
    )

    feedback = discord.ui.TextInput(
        label="Content",
        style=discord.TextStyle.long,
        placeholder="Tag content here...",
        max_length=2000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        """Save tag on submit"""

        await interaction.response.send_message(
            f"Tag '{self.name.value}' successfully created!",
            ephemeral=True
        )

    async def on_error(
            self, error: Exception, interaction: discord.Interaction
    ) -> None:
        """Normally doesn't happens ¯_(ツ)_/¯"""
        await interaction.response.send_message(
            "Oops! Something went wrong.",
            ephemeral=True
        )

        raise error
