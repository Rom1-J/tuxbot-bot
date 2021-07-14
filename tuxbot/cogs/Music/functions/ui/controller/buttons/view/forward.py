from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union

import discord


if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from .....utils import Player, Track


class ForwardButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[Union[discord.PartialEmoji, discord.Emoji, str]]
    row: int

    def __init__(self, row: int, player: Player, track: Track):
        super().__init__(
            emoji="<:forward_10_w:863557551478800384>",
            row=row,
        )

        self._player: Player = player
        self._track: Track = track

    async def callback(self, interaction: discord.Interaction):
        await self._player.forward(interaction)