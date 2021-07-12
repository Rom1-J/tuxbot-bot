from __future__ import annotations
from typing import TYPE_CHECKING

import discord


if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from ....utils import Player, Track


class PreviousButton(discord.ui.Button):
    def __init__(self, row: int, player: Player, track: Track):
        super().__init__(
            emoji="<:prev_song_w:863162971802042400>",
            row=row,
            style=discord.ButtonStyle.primary,
        )

        self._player: Player = player
        self._track: Track = track

    async def callback(self, interaction: discord.Interaction):
        await self._player.back(self._player.context, track=self._track)
