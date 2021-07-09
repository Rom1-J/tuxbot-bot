import asyncio
import datetime
from typing import Optional

import async_timeout
import discord
import wavelink

from tuxbot.core.utils.functions.extra import ContextPlus
from .exceptions import TrackTooLong
from .menus import InteractiveController


def _(x):
    return x


class Track(wavelink.Track):
    """Wavelink Track object with a requester attribute."""

    __slots__ = ("requester", "emoji")

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get("requester")
        self.emoji = self.get_emoji(**kwargs)

    @staticmethod
    def get_emoji(**kwargs) -> str:
        query: str = kwargs.get("query", "")

        transform = {
            "youtube": "<:youtube:862463749273026561>",
            "ytsearch": "<:youtube:862463749273026561>",
            "spotify": "<:spotify:862463903959351309>",
            "soundcloud": "<:soundcloud:862464041121087518>",
        }

        for key, value in transform.items():
            if key in query.replace(".", ""):
                return value

        return "🎵"


class Player(wavelink.Player):
    """Custom wavelink Player class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context: ContextPlus = kwargs.get("context", None)
        if self.context:
            self.dj: discord.Member = self.context.author

        self.queue = asyncio.Queue()
        self.controller = None

        self.waiting = False
        self.updating = False

        self.pause_votes = set()
        self.resume_votes = set()
        self.skip_votes = set()
        self.shuffle_votes = set()
        self.stop_votes = set()

    async def do_next(self) -> None:
        if self.is_playing or self.waiting:
            return

        # Clear the votes for a new song...
        self.pause_votes.clear()
        self.resume_votes.clear()
        self.skip_votes.clear()
        self.shuffle_votes.clear()
        self.stop_votes.clear()

        try:
            self.waiting = True
            with async_timeout.timeout(300):
                track = await self.queue.get()
        except asyncio.TimeoutError:
            # No music has been played for 5 minutes, cleanup and disconnect...
            return await self.teardown()

        await self.play(track)
        self.waiting = False

        # Invoke our players controller...
        await self.invoke_controller()

    async def invoke_controller(self) -> None:
        """Method which updates or sends a new player controller."""
        if self.updating:
            return

        self.updating = True

        if not self.controller:
            self.controller = InteractiveController(
                embed=self.build_embed(), player=self
            )
            await self.controller.start(self.context)

        elif not await self.is_position_fresh():
            try:
                await self.controller.message.delete()
            except discord.HTTPException:
                pass

            self.controller.stop()

            self.controller = InteractiveController(
                embed=self.build_embed(), player=self
            )
            await self.controller.start(self.context)

        else:
            embed = self.build_embed()
            await self.controller.message.edit(content=None, embed=embed)

        self.updating = False

    def build_embed(self) -> Optional[discord.Embed]:
        track = self.current
        if not track:
            return None

        channel = self.bot.get_channel(int(self.channel_id))
        qsize = self.queue.qsize()

        embed = discord.Embed(
            title=f"Music Controller | {channel.name}", colour=0xEBB145
        )
        embed.description = f"Now Playing:\n**`{track.title}`**\n\n"
        embed.set_thumbnail(url=track.thumb)

        embed.add_field(
            name="Duration",
            value=str(datetime.timedelta(milliseconds=int(track.length))),
        )
        embed.add_field(name="Queue Length", value=str(qsize))
        embed.add_field(name="Volume", value=f"**`{self.volume}%`**")
        embed.add_field(name="Requested By", value=track.requester.mention)
        embed.add_field(name="DJ", value=self.dj.mention)
        embed.add_field(name="Video URL", value=f"[Click Here!]({track.uri})")

        return embed

    async def is_position_fresh(self) -> bool:
        """Method which checks whether the player controller should be remade or updated."""
        try:
            async for message in self.context.channel.history(limit=5):
                if message.id == self.controller.message.id:
                    return True
        except (discord.HTTPException, AttributeError):
            return False

        return False

    async def teardown(self):
        """Clear internal states, remove player controller and disconnect."""
        try:
            await self.controller.message.delete()
        except discord.HTTPException:
            pass

        self.controller.stop()

        try:
            await self.destroy()
        except KeyError:
            pass


def check_track_or_raise(track: Track):
    if track.length > 3600 * 2:
        raise TrackTooLong(_("The music should not exceed 2 hours"))
