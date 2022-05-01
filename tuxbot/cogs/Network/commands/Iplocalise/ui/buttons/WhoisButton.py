from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord


if TYPE_CHECKING:
    from ..ViewController import ViewController


class WhoisButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[discord.PartialEmoji]
    row: int

    def __init__(self, row: int, controller: "ViewController"):
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.primary,
            label=self.controller.ctx.prefix + "whois",
            row=row,
            disabled=True,
        )

    async def callback(self, interaction: discord.Interaction):
        ...
