import logging
import datetime
import typing

import discord
import humanize
import wavelink
from discord.ext import commands

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from tuxbot.core.utils.functions.extra import ContextPlus, command_extra
from .functions import listeners
from .functions.converters import QueryConverter
from .functions.exceptions import EmptyChannelException, NoDMException
from .functions.utils import (
    Player,
    Track,
    check_track_or_raise,
)

log = logging.getLogger("tuxbot.cogs.Music")
_ = Translator("Music", __file__)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot: Tux, version_info):
        self.bot = bot
        self.version_info = version_info

        if not hasattr(bot, "wavelink"):
            self.bot.wavelink = wavelink.Client(bot=bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self) -> None:
        await self.bot.wait_until_ready()

        if self.bot.wavelink.nodes:
            previous = self.bot.wavelink.nodes.copy()

            for node in previous.values():
                await node.destroy()

        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2333,
                "rest_uri": "http://127.0.0.1:2333",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "eu_central",
            }
        }

        for n in nodes.values():
            await self.bot.wavelink.initiate_node(**n)

    def cog_check(self, ctx: ContextPlus):
        if not ctx.guild:
            raise NoDMException(
                _(
                    "Voice commands are not available in private messages.",
                    ctx,
                    self.bot.config,
                )
            )

        return True

    # =========================================================================

    async def cog_before_invoke(self, ctx: ContextPlus):
        await listeners.cog_before_invoke(self, ctx)

    async def cog_command_error(self, ctx: ContextPlus, error):
        await listeners.cog_command_error(self, ctx, error)

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node: wavelink.Node):
        await listeners.on_node_ready(self, node)

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node: wavelink.Node, payload):
        await listeners.on_player_stop(self, node, payload)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        await listeners.on_voice_state_update(self, member, before, after)

    # =========================================================================
    # =========================================================================

    @command_extra(name="connect", deletable=False)
    async def _connect(
        self,
        ctx: ContextPlus,
        *,
        channel: typing.Union[
            discord.VoiceChannel, discord.StageChannel
        ] = None,
    ):
        # noinspection PyTypeChecker
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if player.is_connected:
            return

        channel = getattr(ctx.author.voice, "channel", channel)

        if channel is None:
            raise EmptyChannelException

        await player.connect(channel.id)

    # pylint: disable=too-many-branches
    @command_extra(name="play", deletable=False)
    async def _play(self, ctx: ContextPlus, *, query: QueryConverter):
        # noinspection PyTypeChecker
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            await ctx.invoke(self._connect)

        tracks = await self.bot.wavelink.get_tracks(str(query))

        if not tracks:
            return await ctx.send(
                _(
                    "No songs were found with that query. Please try another.",
                    ctx,
                    self.bot.config,
                )
            )

        if isinstance(tracks, wavelink.TrackPlaylist):
            count = 0

            for i, track in enumerate(tracks.tracks):
                prev_track = None
                next_track = None

                if i == 0:
                    if player.queue:
                        prev_track = player.queue[-1]
                    else:
                        prev_track = player.current
                elif i > 0:
                    prev_track = tracks.tracks[i - 1]

                if i < len(tracks.tracks) - 1:
                    next_track = tracks.tracks[i + 1]

                track = Track(
                    track.id,
                    track.info,
                    requester=ctx.author,
                    query=query,
                    previous=prev_track,
                    next=next_track,
                )

                if track.length < 3605 * 2 * 1000:
                    if prev_track and i == 0:
                        prev_track.next = track

                    count += 1
                    player.queue.append(track)

            e = discord.Embed(
                color=0x2F3136,
                description=_(
                    "> **+{count}** new tracks added from the playlist __{name}__",
                    ctx,
                    self.bot.config,
                ).format(
                    count=count,
                    name=tracks.data["playlistInfo"]["name"],
                ),
            )

            await ctx.send(embed=e, delete_after=15)
        else:
            prev_track = None

            if len(player.queue) > 1:
                prev_track = player.queue[-2]

            track = Track(
                tracks[0].id,
                tracks[0].info,
                requester=ctx.author,
                query=query,
                previous=prev_track,
                next=None,
            )
            check_track_or_raise(track)

            e = discord.Embed(
                color=0x2F3136,
                description=_(
                    "> Added __{name}__ to the Queue", ctx, self.bot.config
                ).format(name=track.title),
            )

            if prev_track:
                prev_track.next = track

            player.queue.append(track)

            await ctx.send(embed=e, delete_after=15)

        if not player.is_playing:
            await player.do_next()
        else:
            await player.invoke_controller()

    @command_extra(name="back", deletable=False)
    async def _back(self, ctx: ContextPlus):
        # noinspection PyTypeChecker
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        await player.back(ctx)

    @command_extra(name="skip", deletable=False)
    async def _skip(self, ctx: ContextPlus):
        # noinspection PyTypeChecker
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        await player.skip(ctx)

    @command_extra(name="queue", aliases=["q"], deletable=False)
    async def _queue(self, ctx: ContextPlus):
        # noinspection PyTypeChecker
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        await player.playlist(ctx)

    @command_extra(name="now_playing", aliases=["np"], deletable=False)
    async def _now_playing(self, ctx: ContextPlus):
        # noinspection PyTypeChecker
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        await player.invoke_controller()

    @commands.command(name="player_info", deletable=False)
    async def _player_info(self, ctx):
        """Retrieve various Node/Server/Player information."""
        player = self.bot.wavelink.get_player(ctx.guild.id)
        node = player.node

        used = humanize.naturalsize(node.stats.memory_used)
        total = humanize.naturalsize(node.stats.memory_allocated)
        free = humanize.naturalsize(node.stats.memory_free)
        cpu = node.stats.cpu_cores

        fmt = (
            f"**WaveLink:** `{wavelink.__version__}`\n\n"
            f"Connected to `{len(self.bot.wavelink.nodes)}` nodes.\n"
            f"Best available Node `{self.bot.wavelink.get_best_node().__repr__()}`\n"
            f"`{len(self.bot.wavelink.players)}` players are distributed on nodes.\n"
            f"`{node.stats.players}` players are distributed on server.\n"
            f"`{node.stats.playing_players}` players are playing on server.\n\n"
            f"Server Memory: `{used}/{total}` | `({free} free)`\n"
            f"Server CPU: `{cpu}`\n\n"
            f"Server Uptime: `{datetime.timedelta(milliseconds=node.stats.uptime)}`"
        )
        await ctx.send(fmt)
