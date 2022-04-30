"""
tuxbot.cogs.Auto.commands.AutoQuote.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Toggle auto quotes
"""

import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .models.AutoQuote import AutoQuoteModel


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
        if ctx.invoked_subcommand:
            return

        model = await self.__get_model(guild_id=ctx.guild.id)

        e = discord.Embed(
            title="Auto quote status",
            description=f"Active: {model.activated}",
            colour=self.bot.utils.colors.ONLINE.value
            if model.activated else self.bot.utils.colors.DND.value
        )

        await ctx.send(embed=e)

    @_auto_quote.command(name="toggle")
    async def _auto_quote_toggle(self, ctx: commands.Context):
        model = await self.__get_model(guild_id=ctx.guild.id)

        model.activated = not model.activated
        await model.save()

        if not self.bot.cached_config.get(ctx.guild.id):
            self.bot.cached_config[ctx.guild.id] = {}

        self.bot.cached_config[ctx.guild.id]["AutoQuote"] = model.activated

        e = discord.Embed(
            description=f"Auto quote toggled to {model.activated}",
            colour=self.bot.utils.colors.ONLINE.value
            if model.activated else self.bot.utils.colors.DND.value
        )

        await ctx.send(embed=e)
