from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import discord


if TYPE_CHECKING:
    from ...iplocalise.view import ViewController


class GeoButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[discord.PartialEmoji]
    row: int

    def __init__(self, row: int, controller: "ViewController"):
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.secondary,
            emoji="\N{WORLD MAP}",
            row=row,
            label="geo",
        )

    async def callback(self, interaction: discord.Interaction):
        await self.controller.change_to("geo", interaction)
