"""
tuxbot.cogs.Random.commands.Coin.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Flip a coin
"""
import random

import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class CoinCommand(commands.Cog):
    """Flip a coin"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(name="coin")
    async def _coin(self, ctx: commands.Context):
        e = discord.Embed(
            title=random.choice(["Tail", "Head"]),
            color=self.bot.utils.colors.EMBED_BORDER.value,
        )

        await ctx.send(embed=e)
