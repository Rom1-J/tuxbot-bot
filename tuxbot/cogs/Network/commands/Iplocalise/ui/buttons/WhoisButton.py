from __future__ import annotations

import typing

import discord


if typing.TYPE_CHECKING:
    from ..ViewController import ViewController


class WhoisButton(discord.ui.Button["ViewController"]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController) -> None:
        self.controller = controller
        prefix = self.controller.ctx.prefix or (
            f"<@{self.controller.ctx.bot.user.id}>"
            if self.controller.ctx.bot.user
            else ""
        )

        super().__init__(
            style=discord.ButtonStyle.primary,
            label=prefix + "whois",
            row=row,
            disabled=True,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        ...
