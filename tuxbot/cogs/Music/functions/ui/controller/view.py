from __future__ import annotations
import datetime
from os.path import dirname
from typing import List, Optional, TYPE_CHECKING

import discord

from tuxbot.core.i18n import Translator

from .buttons import ButtonType
from .panels import ViewPanel, JumpPanel

if TYPE_CHECKING:
    # pylint: disable=cyclic-import
    from ...utils import Player, Track


_ = Translator("Music", dirname(dirname(dirname(__file__))))


class ControllerView(discord.ui.View):
    children: List[ButtonType]  # type: ignore

    def __init__(
        self,
        player: Player,
        track: Track,
        author: discord.User,
        action: str = "view",
    ):
        super().__init__()

        self._player: Player = player
        self._track: Track = track

        self._author: discord.User = author

        panel = ViewPanel.buttons
        if action == "jump":
            panel = JumpPanel.buttons

        for x, row in enumerate(panel):
            for button in row:
                self.add_item(
                    button(row=x, player=self._player, track=self._track)
                )

        if action == "view":
            self.set_disabled_buttons()
            self.set_pause_button()

    async def on_timeout(self) -> None:
        if self._player.controller:
            await self._player.controller.delete()

        await self._player.invoke_controller()

    # =========================================================================
    # =========================================================================

    def set_disabled_buttons(self):
        _prev = self.get_button("prev_song_w")
        _next = self.get_button("next_song_w")

        if _prev and not (self._track and self._track.previous):
            _prev.disabled = True

        if _next and not (self._track and self._track.next):
            _next.disabled = True

    # =========================================================================

    def set_pause_button(self):
        if not self._player.is_playing:
            _pause = self.get_button("pause_song_w")

            _pause.emoji = "<:play_song_w:863162951032766494>"

    # =========================================================================

    def get_button(self, name: str) -> Optional[discord.ui.Button]:
        for button in self.children:
            if button.emoji.name == name:  # type: ignore
                return button

        return None

    # =========================================================================

    def build_embed(self) -> Optional[discord.Embed]:
        track: Track = self._track or self._player.queue[-1]

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
                "Requested by {name} | Track: {track_pos}/{total}",
                self._player.context,
                self._player.context.bot.config,
            ).format(
                name=str(track.requester),
                track_pos=str(self._player.track_position),
                total=str(queue_size),
            )
        )

        return e
