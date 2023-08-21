import typing

import discord

from tuxbot.cogs.Network.commands.Iplocalise.ui.view_controller import (
    ViewController,
)


class DeleteButton(discord.ui.Button["ViewController"]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(
        self: typing.Self, row: int, controller: ViewController
    ) -> None:
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.danger,
            row=row,
            emoji="\N{WASTEBASKET}",
            label="delete",
        )

    async def callback(
        self: typing.Self, interaction: discord.Interaction  # noqa: ARG002
    ) -> None:
        await self.controller.delete()
