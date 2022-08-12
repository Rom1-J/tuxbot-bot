from __future__ import annotations

import typing

import discord


if typing.TYPE_CHECKING:
    from ..ViewController import ViewController


class IPInfoButton(discord.ui.Button[ViewController]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController):
        self.controller = controller

        super().__init__(
            label="ipinfo.io",
            disabled=True,
            style=discord.ButtonStyle.link,
            row=row,
            url="https://ipinfo.io/",
        )
