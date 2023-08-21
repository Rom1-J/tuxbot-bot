import typing

import discord

from tuxbot.cogs.Network.commands.Iplocalise.ui.view_controller import (
    ViewController,
)


class GeoButton(discord.ui.Button["ViewController"]):
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
            emoji="\N{WORLD MAP}",
            row=row,
            label="geo",
        )

    async def callback(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        await self.controller.change_page(1, interaction)
