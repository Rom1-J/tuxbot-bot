import logging

import math
from os.path import dirname

from typing import Optional, List, Set

import discord
import wavelink

from tuxbot.core.bot import Tux
from tuxbot.core.utils.functions.extra import ContextPlus
from tuxbot.core.i18n import Translator
from .exceptions import TrackTooLong
from .ui.controller.view import ControllerView
from .ui.queue.view import QueueView

log = logging.getLogger("tuxbot.cogs.Music")
_ = Translator("Music", dirname(__file__))


class Track(wavelink.Track):
    previous: Optional["Track"]
    next: Optional["Track"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get("requester")
        self.emoji = self.get_emoji(kwargs.get("query", ""))

        self.previous = kwargs.get("previous")
        self.next = kwargs.get("next")

    @staticmethod
    def get_emoji(query: str) -> str:
        transform = {
            "youtube": "<:youtube:862463749273026561>",
            "ytsearch": "<:youtube:862463749273026561>",
            "spotify": "<:spotify:862463903959351309>",
            "soundcloud": "<:soundcloud:862464041121087518>",
            "vimeo": "<:vimeo:863181307424407552>",
            "bandcamp": "<:bandcamp:863182155084464138>",
        }

        for key, value in transform.items():
            if key in query.replace(".", ""):
                return value

        return "🎵"

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Track requester="%s" title="%s" previous="%s" next="%s">' % (
            str(self.requester),
            self.title,
            str(self.previous),
            str(self.next),
        )


class Player(wavelink.Player):
    bot: Tux
    controller: Optional[discord.Message]

    track_position: int = -1

    def __init__(self, bot: Tux, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)

        self.context: ContextPlus = kwargs.get("context")
        if self.context:
            self.dj: discord.Member = self.context.author

        self.queue: List[Track] = []
        self.controller: Optional[discord.Message] = None

        self.waiting = False
        self.updating = False

        self.pause_votes: Set[discord.Member] = set()
        self.resume_votes: Set[discord.Member] = set()
        self.back_votes: Set[discord.Member] = set()
        self.skip_votes: Set[discord.Member] = set()
        self.shuffle_votes: Set[discord.Member] = set()
        self.end_votes: Set[discord.Member] = set()
        self.delete_votes: Set[discord.Member] = set()

    async def toggle_pause(self, ctx: ContextPlus):
        await self.context.send(
            "Play/Pause not implemented yet...", delete_after=5
        )

    async def back(self, user: discord.Member, track: Optional[Track] = None):
        await self.context.send("back not implemented yet...", delete_after=5)

    async def skip(self, user: discord.Member, track: Optional[Track] = None):
        await self.context.send("Skip not implemented yet...", delete_after=5)

    async def shuffle(self, user: discord.Member):
        await self.context.send(
            "shuffle not implemented yet...", delete_after=5
        )

    async def end(self, user: discord.Member):
        if self.is_privileged(user):
            self.skip_votes.clear()

            if self.controller:
                await self.controller.delete()
            else:
                await self.terminate()
                return await self.context.send(
                    _(
                        "There was no controller to stop.",
                        self.context,
                        self.bot.config,
                    ),
                    delete_after=20,
                )

            await self.terminate()
            return await self.context.send(
                _(
                    "Disconnected player and killed controller.",
                    self.context,
                    self.bot.config,
                ),
                delete_after=20,
            )

        required = self.required(stop=True)
        self.end_votes.add(user)

        if len(self.skip_votes) >= required:
            await self.context.send(
                _(
                    "Vote to end passed. Ending session.",
                    self.context,
                    self.bot.config,
                ),
                delete_after=10,
            )
            self.skip_votes.clear()
            await self.terminate()
        else:
            await self.context.send(
                _(
                    "{name} has voted to end this session.",
                    self.context,
                    self.bot.config,
                ).format(name=user.mention),
                delete_after=15,
            )

    async def delete(self, user: discord.Member, track: Track):
        await self.context.send(
            "Remove not implemented yet...", delete_after=5
        )

    async def playlist(
        self,
        user: discord.Member,
        interaction: Optional[discord.Interaction] = None,
    ):
        view = QueueView(author=user, player=self)

        if interaction:
            await interaction.response.send_message(
                "Music on hold:", view=view, ephemeral=True
            )
        else:
            await self.context.send("Music on hold:", view=view)

    # =========================================================================
    # =========================================================================

    async def do_next(self) -> None:
        if self.is_playing or self.waiting:
            return

        self.pause_votes.clear()
        self.resume_votes.clear()
        self.skip_votes.clear()
        self.shuffle_votes.clear()
        self.end_votes.clear()

        if self.track_position != -1 and self.track_position < len(self.queue):
            await self.play(self.queue[self.track_position])
            self.waiting = False

            self.track_position += 1
        else:
            print("finish")

        await self.invoke_controller()

    # =========================================================================

    async def invoke_controller(self, force: bool = False) -> None:
        if self.updating:
            return

        self.updating = True

        if not self.controller:
            view = ControllerView(
                author=self.context.author, player=self, track=self.current
            )

            self.controller = await self.context.send(
                embed=view.build_embed(), view=view
            )

        elif force or not await self.is_position_fresh():
            try:
                await self.controller.delete()
            except discord.HTTPException:
                pass

            view = ControllerView(
                author=self.context.author, player=self, track=self.current
            )

            self.controller = await self.context.send(
                embed=view.build_embed(), view=view
            )

        else:
            view = ControllerView(
                author=self.context.author, player=self, track=self.current
            )

            await self.controller.edit(embed=view.build_embed(), view=view)

        self.updating = False

    # =========================================================================

    async def is_position_fresh(self) -> bool:
        if not self.controller:
            return False

        try:
            async for message in self.context.channel.history(limit=5):
                if (
                    isinstance(message, discord.Message)
                    and message.id == self.controller.id
                ):
                    return True
        except (discord.HTTPException, AttributeError):
            return False

        return False

    # =========================================================================

    async def terminate(self) -> None:
        try:
            if self.controller:
                await self.controller.delete()
        except discord.HTTPException:
            pass

        try:
            await self.destroy()
        except KeyError:
            pass

    # =========================================================================

    def is_privileged(self, user: discord.Member) -> bool:
        return self.dj == user or user.guild_permissions.kick_members

    # =========================================================================

    def required(self, stop: bool = False) -> int:
        channel = self.bot.get_channel(
            int(self.channel_id if self.channel_id else 0)
        )
        if not isinstance(
            channel, (discord.VoiceChannel, discord.StageChannel)
        ):
            return -1

        required = math.ceil((len(channel.members) - 1) / 2.5)

        if stop and len(channel.members) == 3:
            required = 2

        return required

    # =========================================================================

    async def back_queue(self, track: Optional[Track]) -> None:
        raise NotImplementedError

    async def skip_queue(self, track: Optional[Track]) -> None:
        raise NotImplementedError

    async def remove_queue(self, track: Track) -> None:
        raise NotImplementedError


def check_track_or_raise(track: Track):
    if track.length > 3605 * 2 * 1000:

        def _(x):
            return x

        raise TrackTooLong(_("The music should not exceed 2 hours"))
