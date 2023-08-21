import typing

import discord

from tuxbot.cogs.Utils.commands.Avatar.ui.view_controller import (
    ViewController,
)


class DeleteButton(discord.ui.Button["ViewController"]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(
        self: typing.Self, row: int, controller: ViewController
    ) -> None:
        self.controller = controller

        super().__init__(
            style=discord.ButtonStyle.danger,
            row=row,
            emoji="\N{WASTEBASKET}",
            label="delete",
        )

    async def callback(
        self: typing.Self, interaction: discord.Interaction
    ) -> None:
        if (
            interaction.user == self.controller.ctx.author
        ) and self.controller.sent_message:
            self.controller.stop()
            await self.controller.sent_message.delete()
