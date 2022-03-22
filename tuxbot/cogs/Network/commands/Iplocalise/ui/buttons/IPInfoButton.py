from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord


if TYPE_CHECKING:
    from ..view import ViewController


class IPInfoButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[discord.PartialEmoji]
    row: int

    def __init__(self, row: int, controller: "ViewController"):
        self.controller = controller

        super().__init__(
            label="ipinfo.io",
            style=discord.ButtonStyle.link,
            row=row,
            url="https://ipinfo.io/" + self.controller.data["ip"],
        )
