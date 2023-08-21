"""Page view controller."""
import typing

import discord
from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.cogs.Auto.commands.AutoPin.models.auto_pin import AutoPinModel

from .modals.pin_threshold_modal import PinThresholdModal
from .pages.global_embed import GlobalEmbed
from .panels import ViewPanel


DATA_TYPE = str | int | float | dict | list


class ViewController(discord.ui.View):
    """View controller."""

    __message: discord.Message | None = None

    def __init__(
        self: typing.Self,
        ctx: commands.Context[TuxbotABC],
        model: AutoPinModel,
    ) -> None:
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

    async def on_timeout(self: typing.Self) -> None:
        """Remove buttons after timeout."""
        self.clear_items()

        await self.edit()

    # =========================================================================

    async def interaction_check(
        self: typing.Self, interaction: discord.Interaction
    ) -> bool:
        """Ensure interaction is piloted by author."""
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

    def get_button(
        self: typing.Self, name: str
    ) -> discord.ui.Button["ViewController"] | None:
        """Get view button."""
        for button in self.children:
            if not isinstance(button, discord.ui.Button):
                continue

            if (button.label == name) or (
                button.emoji and button.emoji.name == name
            ):
                return button

        return None

    # =========================================================================

    async def change_state(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        """Change current state."""
        self.model.activated = not self.model.activated
        await self.model.save()
        await self.cache()

        await self.edit()
        await interaction.response.defer()

    # =========================================================================

    async def set_threshold(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        """Change current threshold."""
        await interaction.response.send_modal(PinThresholdModal(self))

    # =========================================================================
    # =========================================================================

    async def send(self: typing.Self) -> None:
        """Send selected embed."""
        await self.edit()

    # =========================================================================

    async def edit(self: typing.Self) -> None:
        """Edit sent message."""
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

    async def cache(self: typing.Self) -> None:
        """Cache result."""
        if not self.ctx.guild:
            return

        self.ctx.bot.cached_config[self.ctx.guild.id]["AutoPin"] = {
            "activated": self.model.activated,
            "threshold": self.model.threshold,
        }

    # =========================================================================

    async def delete(self: typing.Self) -> None:
        """Delete controller."""
        self.stop()

        if self.__message:
            await self.__message.delete()
