from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import discord


if TYPE_CHECKING:
    from ..view import ViewController


class GlobalButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[discord.PartialEmoji]
    row: int

    def __init__(self, row: int, controller: "ViewController"):
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.secondary,
            emoji="\N{GLOBE WITH MERIDIANS}",
            row=row,
            label="global",
            disabled=True,
        )

    async def callback(self, interaction: discord.Interaction):
        await self.controller.change_to("global", interaction)
