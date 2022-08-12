from __future__ import annotations

import typing

import discord


if typing.TYPE_CHECKING:
    from ..ViewController import ViewController


class ToggleButton(discord.ui.Button[ViewController]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController) -> None:
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.secondary,
            row=row,
            disabled=True,
            label="toggle",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await self.controller.change_state(interaction)
