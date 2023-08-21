import typing

import discord

from tuxbot.cogs.Utils.commands.Avatar.ui.view_controller import (
    ViewController,
)


class GIFButton(discord.ui.Button["ViewController"]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(
        self: typing.Self, row: int, controller: ViewController
    ) -> None:
        self.controller = controller
        asset: discord.Asset = self.controller.data.display_avatar

        is_animated = asset.is_animated()

        super().__init__(
            label="GIF",
            style=discord.ButtonStyle.link,
            row=row,
            disabled=not is_animated,
            url=asset.url,
        )
