from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union

import discord


if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from .....utils import Player, Track


class PreviousButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[Union[discord.PartialEmoji, discord.Emoji, str]]
    row: int

    def __init__(self, row: int, player: Player, track: Track):
        super().__init__(
            emoji="<:prev_song_w:863162971802042400>",
            row=row,
            style=discord.ButtonStyle.primary,
        )

        self._player: Player = player
        self._track: Track = track

    async def callback(
        self, interaction: discord.Interaction  # skipcq: PYL-W0613
    ):
        await self._player.back(interaction.user)
