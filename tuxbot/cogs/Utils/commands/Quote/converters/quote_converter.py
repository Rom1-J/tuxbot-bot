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


_QuoteConverter_T = QuoteMessage | discord.Message


async def _convert(
    ctx: commands.Context[TuxbotABC], argument: str
) -> _QuoteConverter_T:
    if isinstance((user_member := ctx.author), discord.User):
        raise commands.BadArgument

    if (
        message := await commands.MessageConverter().convert(ctx, argument)
    ) and message.channel.permissions_for(user_member).read_message_history:
        return message

    raise commands.BadArgument


class QuoteConverter(commands.Converter[_QuoteConverter_T]):
    """Gives either discord message link format, or text."""

    async def convert(
        self: typing.Self, ctx: commands.Context[TuxbotABC], argument: str
    ) -> _QuoteConverter_T:
        try:
            return await _convert(ctx, argument)
        except commands.BadArgument:
            return QuoteMessage(
                content=argument, author=str(ctx.message.author)
            )
