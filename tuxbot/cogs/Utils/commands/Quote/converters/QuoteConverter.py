"""
tuxbot.cogs.Utils.converters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gives either discord message link format, or text.
"""
import typing

import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC


class QuoteMessage(typing.NamedTuple):
    """Fake discord Message style"""

    content: str
    author: str


ConvertType = typing.Union[QuoteMessage, discord.Message]


class QuoteConverter(commands.Converter[ConvertType]):
    """Gives either discord message link format, or text."""

    async def convert(  # type: ignore[override]
        self, ctx: commands.Context[TuxbotABC], argument: str
    ) -> ConvertType:
        try:
            if (
                message := await commands.MessageConverter().convert(
                    ctx, argument
                )
            ) and message.channel.permissions_for(
                ctx.author  # type: ignore
            ).read_message_history:
                return message

            raise commands.BadArgument
        except commands.BadArgument:
            return QuoteMessage(
                content=argument, author=str(ctx.message.author)
            )
