import typing

import discord

from tuxbot.cogs.Network.commands.Iplocalise.ui.view_controller import (
    ViewController,
)


class WhoisButton(discord.ui.Button["ViewController"]):
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
            label=prefix + "whois",
            row=row,
            disabled=True,
        )

    async def callback(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        ...
