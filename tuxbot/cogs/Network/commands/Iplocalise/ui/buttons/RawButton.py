from __future__ import annotations

import io
import json
import typing

import discord


if typing.TYPE_CHECKING:
    from ..ViewController import ViewController


class RawButton(discord.ui.Button["ViewController"]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController) -> None:
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.secondary,
            emoji="\N{BOOKMARK TABS}",
            row=row,
            label="raw",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            file=discord.File(
                filename="output.json",
                fp=io.BytesIO(json.dumps(self.controller.data).encode()),
            ),
            ephemeral=True,
        )
