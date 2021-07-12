from __future__ import annotations
from typing import TYPE_CHECKING

import discord


if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from ....utils import Player, Track


class EndButton(discord.ui.Button):
    def __init__(self, row: int, player: Player, track: Track):
        super().__init__(
            emoji="<:leave_w:863442392307597363>",
            row=row,
            style=discord.ButtonStyle.danger,
        )

        self._player: Player = player
        self._track: Track = track

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("End...", ephemeral=True)
