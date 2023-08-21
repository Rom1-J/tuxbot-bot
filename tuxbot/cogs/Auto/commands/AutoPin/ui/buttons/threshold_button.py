import typing

import discord

from tuxbot.cogs.Auto.commands.AutoPin.ui.view_controller import (
    ViewController,
)


class ThresholdButton(discord.ui.Button["ViewController"]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(
        self: typing.Self, row: int, controller: ViewController
    ) -> None:
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.secondary,
            row=row,
            disabled=False,
            label="threshold",
        )

    async def callback(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        await self.controller.set_threshold(interaction)
