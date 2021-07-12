from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union

import discord


if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from ....utils import Player, Track


class RemoveButton(discord.ui.Button):
    disabled: bool
    label: str
    emoji: Optional[Union[discord.PartialEmoji, discord.Emoji, str]]
    row: int

    def __init__(self, row: int, player: Player, track: Track):
        super().__init__(
            emoji="<:trash_w:863163000038227998>",
            row=row,
            style=discord.ButtonStyle.danger,
        )

        self._player: Player = player
        self._track: Track = track

    async def callback(
        self, interaction: discord.Interaction  # skipcq: PYL-W0613
    ):
        await interaction.response.send_message("Remove...", ephemeral=True)
