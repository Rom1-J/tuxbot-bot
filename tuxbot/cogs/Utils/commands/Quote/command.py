"""
tuxbot.cogs.Utils.commands.Quote.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Send message as quote format
"""
import discord
from discord import app_commands
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from .converters.QuoteConverter import QuoteConverter
from .Quote import Quote


class QuoteCommand(commands.Cog):
    """Quote a message"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        self.quote_context_menu = app_commands.ContextMenu(
            name="Turn into a quote", callback=self._quote_context_menu
        )
        self.bot.tree.add_command(self.quote_context_menu)

    # =========================================================================

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.quote_context_menu.name, type=self.quote_context_menu.type
        )

    # =========================================================================
    # =========================================================================

    @commands.command(name="quote")
    async def _quote(
        self, ctx: commands.Context[TuxbotABC], *, argument: str
    ) -> None:
        message = await QuoteConverter().convert(ctx, argument)

        quote = Quote(message.content, str(message.author))

        quote_bytes = await quote.generate()
        file = discord.File(quote_bytes, "quote.png")

        await ctx.send(file=file)

    # =========================================================================

    @staticmethod
    async def _quote_context_menu(
        interaction: discord.Interaction, message: discord.Message
    ) -> None:
        quote = Quote(message.content, str(message.author))

        quote_bytes = await quote.generate()
        file = discord.File(quote_bytes, "quote.png")

        await interaction.response.send_message(file=file)
