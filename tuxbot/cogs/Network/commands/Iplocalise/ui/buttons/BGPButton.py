from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord


if TYPE_CHECKING:
    from ..view import ViewController


class BGPButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[discord.PartialEmoji]
    row: int

    def __init__(self, row: int, controller: "ViewController"):
        self.controller = controller

        super().__init__(
            label="BGP toolkit",
            style=discord.ButtonStyle.link,
            row=row,
            url="https://bgp.he.net/AS"
            + self.controller.data["ipwhois"].get("asn", ""),
        )
