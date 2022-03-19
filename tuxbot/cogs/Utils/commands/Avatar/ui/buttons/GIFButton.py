from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord

if TYPE_CHECKING:
    from ..view import ViewController


class GIFButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[discord.PartialEmoji]
    row: int

    def __init__(self, row: int, controller: "ViewController"):
        self.controller = controller

        is_animated = self.controller.data.display_avatar.is_animated()

        # noinspection PyTypeChecker
        super().__init__(
            label="GIF",
            style=discord.ButtonStyle.link,
            row=row,
            disabled=not is_animated,
            url=self.controller.data.display_avatar.with_format(
                "png" if not is_animated else "gif"
            ).url,
        )
