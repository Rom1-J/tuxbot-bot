from __future__ import annotations
from typing import List, TYPE_CHECKING

import discord

from .options import TrackOption
from ...controller.view import ControllerView

if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from ....utils import Player


class QueueSelect(discord.ui.Select):
    placeholder: str
    options: List[TrackOption]

    def __init__(
        self,
        player: Player,
        options: List[List[TrackOption]],
        author: discord.User,
        **kwargs,
    ):
        self._player: Player = player

        self._options = options
        self._page = kwargs.get("page", 0)

        self._author: discord.User = author
        self._ephemeral = kwargs.get("ephemeral", False)

        super().__init__(
            placeholder=f"Page: {self._page + 1}/{len(self._options)}",
            min_values=1,
            max_values=1,
            options=self._options[self._page],
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.data["values"][0] == "next":
            return await self.update_page(interaction, +1)

        if interaction.data["values"][0] == "prev":
            return await self.update_page(interaction, -1)

        view = ControllerView(
            author=interaction.user,
            player=self._player,
            track=self._options[self._page][
                int(interaction.data["values"][0])
            ].track,
        )

        return await interaction.response.send_message(
            embed=view.build_embed(), view=view, ephemeral=True
        )

    # =========================================================================
    # =========================================================================

    def check_author(self, interaction: discord.Interaction):
        return interaction.user == self._author

    # =========================================================================

    async def update_page(self, interaction: discord.Interaction, page: int):

        if self.check_author(interaction):
            self._page += page
            self.placeholder = f"Page: {self._page + 1}/{len(self._options)}"

            self.options = self._options[self._page]

            self.view.clear_items()
            self.view.add_item(self)

            await interaction.response.edit_message(
                content="Music on hold:", view=self.view
            )
        else:
            select = QueueSelect(
                options=self._options,
                author=interaction.user,
                page=self._page + page,
                player=self._player,
                ephemeral=True,
            )

            self.view.clear_items()
            self.view.add_item(select)

            await interaction.response.send_message(
                content="Music on hold:", view=self.view, ephemeral=True
            )
