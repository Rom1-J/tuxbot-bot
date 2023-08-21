"""
tuxbot.cogs.Utils.converters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Gives either discord message link format, or text.
"""
import typing

import discord
from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC


class QuoteMessage(typing.NamedTuple):
    """Fake discord Message style."""

    content: str
    author: str


ConvertType = QuoteMessage | discord.Message


async def _convert(
    ctx: commands.Context[TuxbotABC], argument: str
) -> ConvertType:
    if (
        message := await commands.MessageConverter().convert(ctx, argument)
    ) and message.channel.permissions_for(ctx.author).read_message_history:
        return message

    raise commands.BadArgument


class QuoteConverter(commands.Converter[ConvertType]):
    """Gives either discord message link format, or text."""

    async def convert(
        self: typing.Self, ctx: commands.Context[TuxbotABC], argument: str
    ) -> ConvertType:
        try:
            return await _convert(ctx, argument)
        except commands.BadArgument:
            return QuoteMessage(
                content=argument, author=str(ctx.message.author)
            )
