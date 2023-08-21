import typing

import discord
from jishaku.models import copy_context_with

from tuxbot.cogs.Network.commands.Iplocalise.ui.view_controller import (
    ViewController,
)


class ASNButton(discord.ui.Button["ViewController"]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(
        self: typing.Self, row: int, controller: ViewController
    ) -> None:
        self.controller = controller
        prefix = self.controller.ctx.prefix or (
            f"<@{self.controller.ctx.bot.user.id}>"
            if self.controller.ctx.bot.user
            else ""
        )

        super().__init__(
            style=discord.ButtonStyle.primary,
            label=prefix + "peeringdb",
            row=row,
        )

    async def callback(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        args = "peeringdb " + str(self.controller.get_data("ipwhois", "asn"))
        prefix = self.controller.ctx.prefix or (
            f"<@{self.controller.ctx.bot.user.id}>"
            if self.controller.ctx.bot.user
            else ""
        )

        command_ctx = await copy_context_with(
            self.controller.ctx,
            content=prefix + args,
            author=interaction.user,
        )
        await self.controller.ctx.bot.process_commands(command_ctx.message)
