from __future__ import annotations
from typing import TYPE_CHECKING

import discord


if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from ....utils import Player, Track


class QueueButton(discord.ui.Button):
    def __init__(self, row: int, player: Player, track: Track):
        super().__init__(
            emoji="<:playlist_w:863162933211037726>",
            row=row,
            style=discord.ButtonStyle.primary,
        )

        self._player: Player = player
        self._track: Track = track

    async def callback(self, interaction: discord.Interaction):
        await self._player.playlist(self._player.context)
