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

        self.action = action

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
        await self._player.invoke_controller()

    # =========================================================================
    # =========================================================================

    def set_disabled_buttons(self):
        _prev = self.get_button("prev_song_w")
        _next = self.get_button("next_song_w")

        _vol_up = self.get_button("vol_up_w")
        _vol_down = self.get_button("vol_down_w")

        if _prev and self._player.last_played_position == -1:
            _prev.disabled = True

        if (
            _next
            and self._player.track_position == len(self._player.queue) - 1
        ):
            _next.disabled = True

        if _vol_up and self._player.volume == 100:
            _vol_up.disabled = True

        if _vol_down and self._player.volume == 0:
            _vol_down.disabled = True

    # =========================================================================

    def set_pause_button(self):
        if not self._player.is_playing or self._player.is_paused:
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
        track: Track = (
            self._track or self._player.queue[self._player.track_position]
        )

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
                track_pos=str(self._player.track_position + 1),
                total=str(queue_size),
            )
        )

        return e