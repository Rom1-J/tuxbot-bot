import typing

import discord

from tuxbot.cogs.Utils.commands.Avatar.ui.view_controller import (
    ViewController,
)


class WEBPButton(discord.ui.Button["ViewController"]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(
        self: typing.Self, row: int, controller: ViewController
    ) -> None:
        self.controller = controller
        asset: discord.Asset = self.controller.data.display_avatar.with_format(
            "webp"
        )

        super().__init__(
            label="WEBP",
            style=discord.ButtonStyle.link,
            row=row,
            url=asset.url,
        )
