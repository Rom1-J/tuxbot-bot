from __future__ import annotations
import textwrap
from os.path import dirname
from typing import List, TYPE_CHECKING

import discord

from tuxbot.core.i18n import Translator

from .parts import QueueSelect, TrackOption

if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from ...utils import Player, Track


_ = Translator("Music", dirname(dirname(dirname(__file__))))


class QueueView(discord.ui.View):
    children: List[QueueSelect]

    def __init__(self, player: Player, author: discord.User):
        super().__init__()

        self._player: Player = player
        self._author: discord.User = author

        self.init_select()

    async def on_timeout(self) -> None:
        self.clear_items()
        self.stop()

    # =========================================================================
    # =========================================================================

    def init_select(self):
        select = QueueSelect(
            options=self.gen_options(),
            author=self._author,
            page=0,
            player=self._player,
        )

        self.add_item(select)

    # =========================================================================

    def gen_options(self) -> List[List[TrackOption]]:
        parts: List[List[Track]] = [
            self._player.queue[x : x + 23]
            for x in range(1, len(self._player.queue), 23)
        ]

        options: List[List[TrackOption]] = [[]]
        pages = 0
        i = 0

        for part_id, part in enumerate(parts, start=1):
            for song in part:
                options[pages].append(
                    TrackOption(
                        value=str(i),
                        label=textwrap.shorten(song.author, width=25),
                        description=textwrap.shorten(song.title, width=50),
                        emoji=song.emoji,
                        track=song,
                        default=song == self._player.current,
                    )
                )

                i += 1

            if pages > 0:
                options[pages].append(
                    TrackOption(value="prev", label="Prev...", emoji="➖")
                )

            if part_id < len(parts):
                options[pages].append(
                    TrackOption(value="next", label="Next...", emoji="➕")
                )

            pages += 1
            options.append([])

        if not options[-1]:
            del options[-1]

        return options
