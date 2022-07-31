from __future__ import annotations

from typing import TYPE_CHECKING

import discord


if TYPE_CHECKING:
    from ..ViewController import ViewController


class BGPButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController):
        self.controller = controller

        super().__init__(
            label="BGP toolkit",
            disabled=True,
            style=discord.ButtonStyle.link,
            row=row,
            url="https://bgp.he.net/AS",
        )
