from __future__ import annotations
import datetime
from os.path import dirname
from typing import List, Optional, TYPE_CHECKING

import discord

from tuxbot.core.i18n import Translator

from .buttons import (
    ButtonType,
    BlankButton,
    RemoveButton,
    VolumeUpButton,
    EndButton,
    BackwardButton,
    PreviousButton,
    ToggleButton,
    NextButton,
    ForwardButton,
    ShuffleButton,
    VolumeDownButton,
    QueueButton,
)


if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from ...utils import Player, Track


_ = Translator("Music", dirname(dirname(dirname(__file__))))


class ControllerView(discord.ui.View):
    children: List[ButtonType]  # type: ignore

    def __init__(self, player: Player, track: Track, author: discord.User):
        super().__init__()

        self._player: Player = player
        self._track: Track = track

        self._author: discord.User = author

        panel = [
            [
                BlankButton,
                RemoveButton,
                VolumeUpButton,
                EndButton,
                BlankButton,
            ],
            [
                BackwardButton,
                PreviousButton,
                ToggleButton,
                NextButton,
                ForwardButton,
            ],
            [
                BlankButton,
                ShuffleButton,
                VolumeDownButton,
                QueueButton,
                BlankButton,
            ],
        ]
        for x, row in enumerate(panel):
            for button in row:
                self.add_item(
                    button(row=x, player=self._player, track=self._track)
                )

        self.set_disabled_buttons()

    async def on_timeout(self) -> None:
        if self._player.controller:
            await self._player.controller.delete()

        await self._player.invoke_controller()

    # =========================================================================
    # =========================================================================

    def set_disabled_buttons(self):
        _prev = self.get_button("prev_song_w")
        _next = self.get_button("next_song_w")

        if _prev and not self._track.previous:
            _prev.disabled = True

        if _next and not self._track.next:
            _next.disabled = True

    # =========================================================================

    def get_button(self, name: str) -> Optional[discord.ui.Button]:
        for button in self.children:
            if button.emoji.name == name:  # type: ignore
                return button

        return None

    # =========================================================================

    def build_embed(self) -> Optional[discord.Embed]:
        track: Track = self._track
        if not track:
            return None

        queue_size = len(self._player.queue)

        e = discord.Embed(colour=0x2F3136)
        e.add_field(
            name=f"{track.emoji} {track.author}",
            value=f"[{track.title}]({track.uri})",
            inline=False,
        )
        if track.thumb:
            e.set_image(url=track.thumb)

        e.add_field(
            name=_(
                "Duration",
                self._player.context,
                self._player.context.bot.config,
            ),
            value=str(datetime.timedelta(milliseconds=int(track.length))),
            inline=True,
        )
        e.add_field(
            name="Volume", value=f"**`{self._player.volume}%`**", inline=True
        )
        e.add_field(name="DJ", value=self._player.dj.mention, inline=True)

        e.set_footer(
            text=_(
                "Requested by {name} | Queue length: {total}",
                self._player.context,
                self._player.context.bot.config,
            ).format(
                name=str(track.requester),
                total=str(queue_size),
            )
        )

        return e
