import copy
import textwrap
from typing import List

import discord

from .utils import Track


def generate_playlist_options(
    playlist: List[Track],
) -> List[List[discord.SelectOption]]:
    # noinspection PyTypeChecker
    parts: List[List[Track]] = [
        playlist[x : x + 23] for x in range(0, len(playlist), 23)
    ]
    out: List[List[discord.SelectOption]] = [[]]
    pages = 0
    i = 0

    for part_id, part in enumerate(parts, start=1):
        for song in part:
            out[pages].append(
                discord.SelectOption(
                    value=str(i),
                    label=textwrap.shorten(song.author, width=25),
                    description=textwrap.shorten(song.title, width=50),
                    emoji=song.emoji,
                )
            )

            i += 1

        if pages > 0:
            out[pages].append(
                discord.SelectOption(value="less", label="Prev...", emoji="➖")
            )

        if part_id < len(parts):
            out[pages].append(
                discord.SelectOption(value="more", label="Next...", emoji="➕")
            )

        pages += 1
        out.append([])

    if not out[-1]:
        del out[-1]

    return out


class PlaylistSelect(discord.ui.Select):
    def __init__(self, options: list, author: discord.User):
        self._page = 0
        self._options = options
        self._author = author

        super().__init__(
            custom_id="Some identifier",
            placeholder=f"Page: {self._page + 1}/{len(self._options)}",
            min_values=1,
            max_values=1,
            options=self._options[self._page],
        )

    async def callback(self, interaction: discord.Interaction):
        author = interaction.user == self._author

        if interaction.data["values"][0] == "more":
            self._page += 1
            self.placeholder = f"Page: {self._page + 1}/{len(self._options)}"

            self.options = self._options[self._page]

        elif interaction.data["values"][0] == "less":
            self._page -= 1
            self.placeholder = f"Page: {self._page + 1}/{len(self._options)}"

            self.options = self._options[self._page]

        view = discord.ui.View()
        view.add_item(copy.copy(self))

        if author:
            await interaction.message.edit(view=view)
        else:
            await interaction.response.send_message(
                content="Music on hold:", view=view, ephemeral=True
            )
