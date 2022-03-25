"""
tuxbot.cogs.Utils.commands.Quote.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Send message as quote format
"""
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .converters.QuoteConverter import QuoteConverter
from .Quote import Quote


class QuoteCommand(commands.Cog):
    """Quote a message"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(name="quote")
    async def _quote(self, ctx: commands.Context, *, message: QuoteConverter):
        # noinspection PyUnresolvedReferences
        quote = Quote(message.content, str(message.author))

        quote_bytes = await quote.generate()
        file = discord.File(quote_bytes, "quote.png")

        await ctx.send(file=file)
