import io
import json
import typing

import discord

from tuxbot.cogs.Network.commands.Iplocalise.ui.view_controller import (
    ViewController,
)


class RawButton(discord.ui.Button["ViewController"]):
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
            emoji="\N{BOOKMARK TABS}",
            row=row,
            label="raw",
        )

    async def callback(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        await interaction.response.send_message(
            file=discord.File(
                filename="output.json",
                fp=io.BytesIO(json.dumps(self.controller.data).encode()),
            ),
            ephemeral=True,
        )
