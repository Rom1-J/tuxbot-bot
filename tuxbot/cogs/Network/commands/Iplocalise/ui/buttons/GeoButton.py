from __future__ import annotations

from typing import TYPE_CHECKING

import discord


if TYPE_CHECKING:
    from ..ViewController import ViewController


class GeoButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController):
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.secondary,
            emoji="\N{WORLD MAP}",
            row=row,
            label="geo",
        )

    async def callback(self, interaction: discord.Interaction):
        await self.controller.change_page(1, interaction)
