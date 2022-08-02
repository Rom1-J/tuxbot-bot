"""
tuxbot.cogs.Auto.commands.AutoQuote.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Toggle auto quotes
"""

from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .models.AutoQuote import AutoQuoteModel
from .ui.ViewController import ViewController


class AutoQuoteCommand(commands.Cog):
    """Toggle auto quotes"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @staticmethod
    async def __get_model(guild_id: int) -> AutoQuoteModel:
        if not (model := await AutoQuoteModel.get_or_none(guild_id=guild_id)):
            model = await AutoQuoteModel.create(guild_id=guild_id)

        return model

    # =========================================================================
    # =========================================================================

    @commands.group(name="auto_quote")
    @commands.guild_only()
    async def _auto_quote(self, ctx: commands.Context):
        await ViewController(
            ctx=ctx,
            model=await self.__get_model(guild_id=ctx.guild.id),
        ).send()
