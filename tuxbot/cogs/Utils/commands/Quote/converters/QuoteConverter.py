"""
tuxbot.cogs.Utils.converters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gives either discord message link format, or text.
"""

from discord.ext import commands
from discord.ext.commands import Context


class QuoteMessage:
    """Fake discord Message style"""

    content: str
    author: str


class QuoteConverter(commands.Converter):
    """Gives either discord message link format, or text."""

    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        try:
            if (
                message := await commands.MessageConverter().convert(
                    ctx, argument
                )
            ) and message.channel.permissions_for(
                ctx.author
            ).read_message_history:
                return message

            raise commands.BadArgument
        except commands.BadArgument:
            message = QuoteMessage()

            message.content = argument
            message.author = str(ctx.message.author)

            return message
