"""
Page view controller
"""
from typing import Union

import discord
from discord.ext import commands

from ..models.AutoQuote import AutoQuoteModel
from .pages.GlobalEmbed import GlobalEmbed
from .panels import ViewPanel


DATA_TYPE = Union[str, int, float, dict, list]


class ViewController(discord.ui.View):
    """View controller"""

    __message: discord.Message = None

    def __init__(self, ctx: commands.Context, model: AutoQuoteModel):
        super().__init__(timeout=60)

        self.ctx = ctx

        self.model = model
        self.embed = GlobalEmbed(self)

        panel = ViewPanel.buttons

        for x, row in enumerate(panel):
            for button in row:
                self.add_item(button(row=x, controller=self))

    # =========================================================================
    # =========================================================================

    async def on_timeout(self) -> None:
        """Remove buttons after timeout"""

        self.clear_items()

        await self.edit()

    # =========================================================================

    async def interaction_check(
        self, interaction: discord.Interaction
    ) -> bool:
        """Ensure interaction is piloted by author"""

        if (
            interaction.user
            and self.ctx.author
            and interaction.user.id == self.ctx.author.id
        ):
            return True

        await interaction.response.send_message(
            "You aren't the author of this interaction.", ephemeral=True
        )
        return False

    # =========================================================================
    # =========================================================================

    def get_button(self, name: str) -> discord.ui.Item | None:
        """Get view button"""

        for button in self.children:  # type: ignore
            if (button.label == name) or (  # type: ignore
                button.emoji and button.emoji.name == name  # type: ignore
            ):  # type: ignore
                return button

        return None

    # =========================================================================

    async def change_state(self, interaction: discord.Interaction):
        """Change current page"""

        self.model.activated = not self.model.activated
        await self.model.save()
        await self.cache()

        await self.edit()
        await interaction.response.defer()

    # =========================================================================
    # =========================================================================

    async def send(self):
        """Send selected embed"""

        await self.edit()

    # =========================================================================

    async def edit(self):
        """Edit sent message"""
        embed = self.embed.rebuild()

        if button := self.get_button("toggle"):
            button.disabled = False
            button.style = (
                discord.ButtonStyle.danger
                if self.model.activated
                else discord.ButtonStyle.success
            )

        if self.__message:
            await self.__message.edit(embed=embed, view=self)
            return

        self.__message = await self.ctx.send(embed=embed, view=self)

    # =========================================================================

    async def cache(self):
        """Cache result"""
        if not self.ctx.bot.cached_config.get(self.ctx.guild.id):
            self.ctx.bot.cached_config[self.ctx.guild.id] = {}

        self.ctx.bot.cached_config[self.ctx.guild.id][
            "AutoQuote"
        ] = self.model.activated

    # =========================================================================

    async def delete(self):
        """Delete controller"""
        self.stop()
        await self.__message.delete()
