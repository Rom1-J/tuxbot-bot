from __future__ import annotations

import typing

import discord


if typing.TYPE_CHECKING:
    from ..ViewController import ViewController


class JPGButton(discord.ui.Button[ViewController]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController):
        self.controller = controller
        asset: discord.Asset = self.controller.data.display_avatar.with_format(
            "jpg"
        )

        super().__init__(
            label="JPG",
            style=discord.ButtonStyle.link,
            row=row,
            url=asset.url,
        )
