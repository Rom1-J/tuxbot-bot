from __future__ import annotations

import typing

import discord


if typing.TYPE_CHECKING:
    from ..ViewController import ViewController


class GeoButton(discord.ui.Button["ViewController"]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController) -> None:
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.secondary,
            emoji="\N{WORLD MAP}",
            row=row,
            label="geo",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.controller.change_page(1, interaction)
