from __future__ import annotations

from typing import TYPE_CHECKING

import discord


if TYPE_CHECKING:
    from ..view import ViewController


class PNGButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController):
        self.controller = controller

        super().__init__(
            label="PNG",
            style=discord.ButtonStyle.link,
            row=row,
            url=self.controller.data.display_avatar.with_format("png").url,
        )
