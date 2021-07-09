import logging
import datetime
import math
import typing

import discord
import humanize
import wavelink
from discord.ext import commands

from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from tuxbot.core.utils.functions.extra import ContextPlus, command_extra
from .converters import QueryConverter
from .functions import listeners
from .functions.exceptions import EmptyChannelException, NoDMException
from .functions.ui import PlaylistSelect, ControllerView
from .functions.utils import (
    Player,
    Track,
    check_track_or_raise,
    generate_playlist_options,
)

log = logging.getLogger("tuxbot.cogs.Vocal")
_ = Translator("Vocal", __file__)


class Vocal(commands.Cog, wavelink.WavelinkMixin):
    """Music Cog."""

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

    def required(self, ctx: ContextPlus):
        # noinspection PyTypeChecker
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )
        channel = self.bot.get_channel(int(player.channel_id))
        if not isinstance(
            channel, (discord.VoiceChannel, discord.StageChannel)
        ):
            return None

        required = math.ceil((len(channel.members) - 1) / 2.5)

        if ctx.command.name == "stop" and len(channel.members) == 3:
            required = 2

        return required

    def is_privileged(self, ctx: ContextPlus):
        # noinspection PyTypeChecker
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        return (
            player.dj == ctx.author
            or ctx.author.guild_permissions.kick_members
        )

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

            for track in tracks.tracks:
                track = Track(
                    track.id, track.info, requester=ctx.author, query=query
                )

                if track.length < 3600 * 2 * 1000:
                    count += 1
                    await player.queue.put(track)

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
            track = Track(
                tracks[0].id, tracks[0].info, requester=ctx.author, query=query
            )
            check_track_or_raise(track)

            e = discord.Embed(
                color=0x2F3136,
                description=_(
                    "> Added __{name}__ to the Queue", ctx, self.bot.config
                ).format(name=track.title),
            )

            await ctx.send(embed=e, delete_after=15)
            await player.queue.put(track)

        if not player.is_playing:
            await player.do_next()

    @command_extra(name="skip", deletable=False)
    async def _skip(self, ctx: ContextPlus):
        # noinspection PyTypeChecker
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send(
                "An admin or DJ has skipped the song.", delete_after=10
            )
            player.skip_votes.clear()

            return await player.stop()

        if ctx.author == player.current.requester:
            await ctx.send(
                "The song requester has skipped the song.", delete_after=10
            )
            player.skip_votes.clear()

            return await player.stop()

        required = self.required(ctx)
        player.skip_votes.add(ctx.author)

        if len(player.skip_votes) >= required:
            await ctx.send(
                "Vote to skip passed. Skipping song.", delete_after=10
            )
            player.skip_votes.clear()
            await player.stop()
        else:
            await ctx.send(
                f"{ctx.author.mention} has voted to skip the song.",
                delete_after=15,
            )

    @command_extra(name="queue", aliases=["q"], deletable=False)
    async def _queue(self, ctx: ContextPlus):
        # noinspection PyTypeChecker
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if player.queue.qsize() == 0:
            return await ctx.send(
                "There are no more songs in the queue.", delete_after=15
            )

        # noinspection PyProtectedMember
        entries = list(player.queue._queue)  # pylint: disable=protected-access

        view = discord.ui.View()
        view.add_item(
            PlaylistSelect(generate_playlist_options(entries), ctx.author)
        )

        await ctx.send("Music on hold:", view=view)

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

    @commands.command(name="test_player", deletable=False)
    async def _test_player(self, ctx: ContextPlus):
        # noinspection PyTypeChecker
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )
        view = ControllerView(author=ctx.author, player=player)

        await ctx.send(
            embed=view.build_embed(),
            view=view
        )
