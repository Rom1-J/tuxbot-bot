from __future__ import annotations
from typing import TYPE_CHECKING

import discord


if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from ....utils import Player, Track


class VolumeUpButton(discord.ui.Button):
    def __init__(self, row: int, player: Player, track: Track):
        super().__init__(
            emoji="<:vol_up_w:863163026470076447>",
            row=row,
            style=discord.ButtonStyle.primary,
        )

        self._player: Player = player
        self._track: Track = track

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("vol up...", ephemeral=True)


class VolumeDownButton(discord.ui.Button):
    def __init__(self, row: int, player: Player, track: Track):
        super().__init__(
            emoji="<:vol_down_w:863163012927848484>",
            row=row,
            style=discord.ButtonStyle.primary,
        )

        self._player: Player = player
        self._track: Track = track

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("vol down...", ephemeral=True)
