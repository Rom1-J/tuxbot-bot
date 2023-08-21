"""
tuxbot.cogs.Random.commands.Coin.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Flip a coin
"""
import random
import typing

import discord
from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.core.tuxbot import Tuxbot


class CoinCommand(commands.Cog):
    """Flip a coin."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(name="coin")
    async def _coin(
        self: typing.Self, ctx: commands.Context[TuxbotABC]
    ) -> None:
        e = discord.Embed(
            title=random.choice(["Tail", "Head"]),  # noqa: S311
            color=self.bot.utils.colors.EMBED_BORDER,
        )

        await ctx.send(embed=e)
