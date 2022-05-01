from __future__ import annotations

import io
import json
from typing import TYPE_CHECKING, Optional

import discord


if TYPE_CHECKING:
    from ..ViewController import ViewController


class RawButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[discord.PartialEmoji]
    row: int

    def __init__(self, row: int, controller: "ViewController"):
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.secondary,
            emoji="\N{BOOKMARK TABS}",
            row=row,
            label="raw",
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            file=discord.File(
                filename="output.json",
                fp=io.BytesIO(json.dumps(self.controller.data).encode())
            ),
            ephemeral=True
        )
