from os.path import dirname

import discord
import wavelink
from tuxbot.cogs.Vocal.functions.utils import Player

from tuxbot.core.i18n import Translator
from tuxbot.core.utils.functions.extra import ContextPlus
from .exceptions import VocalException, IncorrectChannelException

_ = Translator("Vocal", dirname(__file__))


async def cog_before_invoke(self, ctx: ContextPlus):
    player: Player = self.bot.wavelink.get_player(
        ctx.guild.id, cls=Player, context=ctx
    )

    if player.context and player.context.channel != ctx.channel:
        raise IncorrectChannelException(
            _(
                "{author}, you must be in {channel} for this session.",
                ctx,
                self.bot.config,
            ).format(
                author=ctx.author.mention,
                channel=player.context.channel.mention,
            )
        )

    if (
        (ctx.command.name == "connect" and not player.context)
        or self.is_privileged(ctx)
        or not player.channel_id
    ):
        return

    channel = self.bot.get_channel(int(player.channel_id))
    if not channel:
        return

    if player.is_connected and ctx.author not in channel.members:
        raise IncorrectChannelException(
            _(
                "{author}, you must be in {channel} to use voice commands.",
                ctx,
                self.bot.config,
            ).format(
                author=ctx.author.mention,
                channel=player.context.channel.mention,
            )
        )


async def cog_command_error(self, ctx, error):
    if isinstance(error, VocalException):
        await ctx.send(_(str(error), ctx, self.bot.config))


async def on_node_ready(self, node: wavelink.Node):
    self.bot.console.log(f"Node {node.identifier} is ready!")


# pylint: disable=unused-argument
async def on_player_stop(
    self, node: wavelink.Node, payload: wavelink.TrackEnd
):
    await payload.player.do_next()


# pylint: disable=unused-argument
async def on_voice_state_update(
    self,
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState,
):
    if member.bot:
        return

    player: Player = self.bot.wavelink.get_player(member.guild.id, cls=Player)

    if not player.channel_id or not player.context:
        player.node.players.pop(member.guild.id)
        return

    channel = self.bot.get_channel(int(player.channel_id))

    if member == player.dj and after.channel is None:
        for m in channel.members:
            if m.bot:
                continue

            player.dj = m
            return

    elif after.channel == channel and player.dj not in channel.members:
        player.dj = member
