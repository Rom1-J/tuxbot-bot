import asyncio
import textwrap
from os.path import dirname

from typing import Optional, List

import async_timeout
import discord
import math
import wavelink

from tuxbot.core.bot import Tux
from tuxbot.core.utils.functions.extra import ContextPlus
from tuxbot.core.i18n import Translator
from .exceptions import TrackTooLong
from .ui import ControllerView

_ = Translator("Vocal", dirname(__file__))


class Track(wavelink.Track):
    """Wavelink Track object with a requester attribute."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get("requester")
        self.emoji = self.get_emoji(kwargs.get("query", ""))

        self.previous: Optional[Track] = kwargs.get("previous", None)
        self.next: Optional[Track] = kwargs.get("next", None)

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

    def __init__(self, bot: Tux, *args, **kwargs):
        super().__init__(bot, *args, **kwargs)

        self.context: ContextPlus = kwargs.get("context", None)
        if self.context:
            self.dj: discord.Member = self.context.author

        self.queue: List[Track] = list()
        self.controller: Optional[discord.Message] = None

        self.waiting = False
        self.updating = False

        self.pause_votes = set()
        self.resume_votes = set()
        self.skip_votes = set()
        self.shuffle_votes = set()
        self.end_votes = set()
        self.delete_votes = set()

    async def pause(self, ctx: ContextPlus):
        raise NotImplementedError

    async def resume(self, ctx: ContextPlus):
        raise NotImplementedError

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

            try:
                await self.controller.delete()
            except KeyError:
                await self.disconnect()
                return await ctx.send(
                    _(
                        "There was no controller to stop.",
                        ctx,
                        self.bot.config,
                    ),
                    delete_after=20,
                )

            await self.disconnect()
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
            await self.disconnect()
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
                track = self.queue.pop(0)
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

            await self.controller.message.edit(
                embed=view.build_embed(), view=view
            )

        self.updating = False

    # =========================================================================

    async def is_position_fresh(self) -> bool:
        try:
            async for message in self.context.channel.history(limit=5):
                if message.id == self.controller.message.id:
                    return True
        except (discord.HTTPException, AttributeError):
            return False

        return False

    # =========================================================================

    async def terminate(self) -> None:
        try:
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

    def skip_queue(self, track: Optional[Track]) -> None:
        if track:
            new_queue = self.queue[self.queue.index(track) :]
            new_queue[0].previous = None

            self.queue = new_queue.copy()


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


def check_track_or_raise(track: Track):
    if track.length > 3600 * 2 * 1000:

        def _(x):
            return x

        raise TrackTooLong(_("The music should not exceed 2 hours"))
