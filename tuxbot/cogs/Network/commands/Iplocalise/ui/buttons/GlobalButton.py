from __future__ import annotations

from typing import TYPE_CHECKING

import discord


if TYPE_CHECKING:
    from ..ViewController import ViewController


class GlobalButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController):
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.secondary,
            emoji="\N{GLOBE WITH MERIDIANS}",
            row=row,
            label="global",
        )

    async def callback(self, interaction: discord.Interaction):
        await self.controller.change_page(0, interaction)
