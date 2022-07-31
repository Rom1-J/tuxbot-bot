from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from jishaku.models import copy_context_with


if TYPE_CHECKING:
    from ..ViewController import ViewController


class ASNButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(self, row: int, controller: ViewController):
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.primary,
            label=self.controller.ctx.prefix + "peeringdb",
            row=row,
        )

    async def callback(self, interaction: discord.Interaction):
        args = "peeringdb " + str(self.controller.get_data("ipwhois", "asn"))

        command_ctx = await copy_context_with(
            self.controller.ctx,
            content=self.controller.ctx.prefix + args,
            author=interaction.user,
        )
        await self.controller.ctx.bot.process_commands(command_ctx.message)
