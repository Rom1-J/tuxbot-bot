"""AutoPin threshold configuration view."""
import typing

import discord


if typing.TYPE_CHECKING:
    from tuxbot.cogs.Auto.commands.AutoPin.ui.view_controller import (
        ViewController,
    )


class PinThresholdModal(discord.ui.Modal):
    """Tag creation modal."""

    title = "Set the threshold"

    def __init__(self: typing.Self, view: "ViewController") -> None:
        super().__init__()

        self.view = view

        self.threshold: discord.ui.TextInput[
            PinThresholdModal
        ] = discord.ui.TextInput(
            label="Threshold",
            placeholder="How many reaction to add for pin...",
        )

        self.add_item(self.threshold)

    # =========================================================================
    # =========================================================================

    async def on_submit(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        """Save threshold on submit."""
        if not interaction.guild:
            return

        if not self.threshold.value.isdigit() or (
            (threshold := int(self.threshold.value)) < 2 or threshold > 9999
        ):
            await interaction.response.send_message(
                "The threshold must be between 2 and 9999",
                ephemeral=True,
            )
            return

        self.view.model.threshold = threshold
        await self.view.model.save()

        await self.view.cache()

        await self.view.edit()
        await interaction.response.defer()
