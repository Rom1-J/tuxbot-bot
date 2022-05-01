from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord


if TYPE_CHECKING:
    from ..ViewController import ViewController


class DeleteButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[discord.PartialEmoji]
    row: int

    def __init__(self, row: int, controller: "ViewController"):
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.danger,
            row=row,
            emoji="\N{WASTEBASKET}",
            label="delete",
        )

    async def callback(self, interaction: discord.Interaction):
        await self.controller.delete()
