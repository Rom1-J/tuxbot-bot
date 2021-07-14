from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union

import discord


if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from .....utils import Player, Track


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

    async def callback(self, interaction: discord.Interaction):
        await self._player.delete(interaction.user, track=self._track)

        if self.view.action == "jump":
            self.view.stop()

            await interaction.response.edit_message(
                content="<:blank:863085374640488518>", view=None
            )
