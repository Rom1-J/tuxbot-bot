from discord.ext import commands
from discord.ext.commands import Context


class QuoteMessage:
    content: str
    author: str


class QuoteConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        try:
            return await commands.MessageConverter().convert(ctx, argument)
        except commands.BadArgument:
            message = QuoteMessage()

            message.content = argument
            message.author = str(ctx.message.author)

            return message
