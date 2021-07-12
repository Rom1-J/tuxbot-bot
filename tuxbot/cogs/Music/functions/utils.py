import asyncio
import math
from os.path import dirname

from typing import Optional, List, Set

import async_timeout
import discord
import wavelink

from tuxbot.core.bot import Tux
from tuxbot.core.utils.functions.extra import ContextPlus
from tuxbot.core.i18n import Translator
from .exceptions import TrackTooLong
from .ui.controller.view import ControllerView
from .ui.queue.view import QueueView

_ = Translator("Music", dirname(__file__))


class Track(wavelink.Track):
    previous: Optional["Track"]
    next: Optional["Track"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get("requester")
        self.emoji = self.get_emoji(kwargs.get("query", ""))

        self.previous = kwargs.get("previous", None)
        self.next = kwargs.get("next", None)

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


class Player(wavelink.Player):
    bot: Tux
    controller: Optional[discord.Message]

    def __init__(self, bot: Tux, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)

        self.context: ContextPlus = kwargs.get("context", None)
        if self.context:
            self.dj: discord.Member = self.context.author

        self.queue: List[Track] = list()
        self.controller: Optional[discord.Message] = None

        self.waiting = False
        self.updating = False

        self.pause_votes: Set[discord.User] = set()
        self.resume_votes: Set[discord.User] = set()
        self.back_votes: Set[discord.User] = set()
        self.skip_votes: Set[discord.User] = set()
        self.shuffle_votes: Set[discord.User] = set()
        self.end_votes: Set[discord.User] = set()
        self.delete_votes: Set[discord.User] = set()

    async def pause(self, ctx: ContextPlus):
        raise NotImplementedError

    async def resume(self, ctx: ContextPlus):
        raise NotImplementedError

    async def back(self, ctx: ContextPlus, track: Optional[Track] = None):
        if not self.is_connected:
            return

        if not self.current.previous:
            return await ctx.send(
                _("There is not previous song...", ctx, self.bot.config)
            )

        if track:
            huge_back = _(
                " directly to __{name}__.", ctx, self.bot.config
            ).format(name=track.title)
        else:
            huge_back = "."

        if self.is_privileged(ctx):
            await ctx.send(
                _(
                    "An admin or DJ has came back on the song",
                    ctx,
                    self.bot.config,
                )
                + huge_back,
                delete_after=10,
            )
            self.back_votes.clear()

            self.back_queue(track)
            return await self.stop()

        if ctx.author == self.current.requester:
            await ctx.send(
                _(
                    "The song requester has came back on the song",
                    ctx,
                    self.bot.config,
                )
                + huge_back,
                delete_after=10,
            )
            self.back_votes.clear()

            self.back_queue(track)
            return await self.stop()

        required = self.required()
        self.skip_votes.add(ctx.author)

        if len(self.skip_votes) >= required:
            await ctx.send(
                _("Vote to came back passed. Came back", ctx, self.bot.config)
                + huge_back,
                delete_after=10,
            )
            self.back_votes.clear()
            self.back_queue(track)
            await self.stop()
        else:
            await ctx.send(
                _(
                    "{name} has voted to came back on the song",
                    ctx,
                    self.bot.config,
                ).format(name=ctx.author.mention)
                + huge_back,
                delete_after=15,
            )

    async def skip(self, ctx: ContextPlus, track: Optional[Track] = None):
        if not self.is_connected:
            return

        if track:
            huge_skip = _(
                " directly to __{name}__.", ctx, self.bot.config
            ).format(name=track.title)
        else:
            huge_skip = "."

        if self.is_privileged(ctx):
            await ctx.send(
                _("An admin or DJ has skipped the song", ctx, self.bot.config)
                + huge_skip,
                delete_after=10,
            )
            self.skip_votes.clear()

            self.skip_queue(track)
            return await self.stop()

        if ctx.author == self.current.requester:
            await ctx.send(
                _(
                    "The song requester has skipped the song",
                    ctx,
                    self.bot.config,
                )
                + huge_skip,
                delete_after=10,
            )
            self.skip_votes.clear()

            self.skip_queue(track)
            return await self.stop()

        required = self.required()
        self.skip_votes.add(ctx.author)

        if len(self.skip_votes) >= required:
            await ctx.send(
                _("Vote to skip passed. Skipping song", ctx, self.bot.config)
                + huge_skip,
                delete_after=10,
            )
            self.skip_votes.clear()
            await self.stop()
        else:
            await ctx.send(
                _(
                    "{name} has voted to skip the song", ctx, self.bot.config
                ).format(name=ctx.author.mention)
                + huge_skip,
                delete_after=15,
            )

    async def shuffle(self, ctx: ContextPlus):
        raise NotImplementedError

    async def end(self, ctx: ContextPlus):
        if self.is_privileged(ctx):
            self.skip_votes.clear()

            if self.controller:
                await self.controller.delete()
            else:
                await self.terminate()
                return await ctx.send(
                    _(
                        "There was no controller to stop.",
                        ctx,
                        self.bot.config,
                    ),
                    delete_after=20,
                )

            await self.terminate()
            return await ctx.send(
                _(
                    "Disconnected player and killed controller.",
                    ctx,
                    self.bot.config,
                ),
                delete_after=20,
            )

        required = self.required(stop=True)
        self.end_votes.add(ctx.author)

        if len(self.skip_votes) >= required:
            await ctx.send(
                _("Vote to end passed. Ending session.", ctx, self.bot.config),
                delete_after=10,
            )
            self.skip_votes.clear()
            await self.terminate()
        else:
            await ctx.send(
                _(
                    "{name} has voted to end this session",
                    ctx,
                    self.bot.config,
                ).format(name=ctx.author.mention),
                delete_after=15,
            )

    async def delete(self, ctx: ContextPlus, track: Track):
        raise NotImplementedError

    async def playlist(self, ctx: ContextPlus):
        view = QueueView(author=ctx.author, player=self)

        await ctx.send("Music on hold:", view=view)

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

        try:
            self.waiting = True
            with async_timeout.timeout(120):
                track = self.queue[0]
        except asyncio.TimeoutError:
            return await self.terminate()

        await self.play(track)
        self.waiting = False

        await self.invoke_controller()

    # =========================================================================

    async def invoke_controller(self) -> None:
        if self.updating:
            return

        self.updating = True

        if len(self.queue) > 1:
            self.queue[0].next = self.queue[1]
            self.queue[1].previous = self.queue[0]

        if not self.controller:
            view = ControllerView(
                author=self.context.author, player=self, track=self.current
            )

            self.controller = await self.context.send(
                embed=view.build_embed(), view=view
            )

        elif not await self.is_position_fresh():
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

    def is_privileged(self, ctx: ContextPlus) -> bool:
        return (
            self.dj == ctx.author or ctx.author.guild_permissions.kick_members
        )

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

    def back_queue(self, track: Optional[Track]) -> None:
        if track:
            new_queue = [None, track.previous] + self.queue[
                self.queue.index(track) :
            ]  # type: ignore

            self.queue = new_queue  # type: ignore
        else:
            new_queue = [None, self.current.previous] + self.queue  # type: ignore

            self.queue = new_queue  # type: ignore

    def skip_queue(self, track: Optional[Track]) -> None:
        if track:
            new_queue = self.queue[self.queue.index(track) :]

            self.queue = new_queue  # type: ignore


def check_track_or_raise(track: Track):
    if track.length > 3605 * 2 * 1000:

        def _(x):
            return x

        raise TrackTooLong(_("The music should not exceed 2 hours"))
