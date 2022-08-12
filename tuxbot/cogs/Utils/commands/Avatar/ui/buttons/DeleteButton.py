from __future__ import annotations

import typing

import discord


if typing.TYPE_CHECKING:
    from ..ViewController import ViewController


class DeleteButton(discord.ui.Button[ViewController]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController):
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.danger,
            row=row,
            emoji="\N{WASTEBASKET}",
            label="delete",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if (
            interaction.user == self.controller.ctx.author
        ) and self.controller.sent_message:
            self.controller.stop()
            await self.controller.sent_message.delete()
