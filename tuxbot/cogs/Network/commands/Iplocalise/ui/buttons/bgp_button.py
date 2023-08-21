import typing

import discord

from tuxbot.cogs.Network.commands.Iplocalise.ui.view_controller import (
    ViewController,
)


class BGPButton(discord.ui.Button["ViewController"]):
    disabled: bool
    label: str
    emoji: discord.PartialEmoji | None
    row: int

    def __init__(
        self: typing.Self, row: int, controller: ViewController
    ) -> None:
        self.controller = controller

        super().__init__(
            label="BGP toolkit",
            disabled=True,
            style=discord.ButtonStyle.link,
            row=row,
            url="https://bgp.he.net/AS",
        )
