from __future__ import annotations
from typing import TYPE_CHECKING, Union, Optional

import discord


if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from .....utils import Player, Track


class ToggleButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[Union[discord.PartialEmoji, discord.Emoji, str]]
    row: int

    def __init__(self, row: int, player: Player, track: Track):
        super().__init__(
            emoji="<:pause_song_w:863162917595906048>",
            row=row,
            style=discord.ButtonStyle.primary,
        )

        self._player: Player = player
        self._track: Track = track

    async def callback(self, interaction: discord.Interaction):
        await self._player.toggle_pause(interaction.user)
