"""
tuxbot.cogs.Math.commands.factor.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Decompose given number in prime factors
"""
import asyncio
import typing

from discord.ext import commands
from sympy import factorint, pretty

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.cogs.Math.converters.expr_converter import ExprConverter
from tuxbot.core.tuxbot import Tuxbot


def _factors_result(n: int) -> str:
    return " + ".join([f"{k}**{v}" for k, v in factorint(n).items()])


class FactorCommand(commands.Cog):
    """Decompose in prime factors."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __factors_result(
        ctx: commands.Context[TuxbotABC], n: int
    ) -> str:
        """Generate prime factor decomposition of n."""
        try:
            output = await asyncio.wait_for(
                asyncio.get_running_loop().run_in_executor(
                    None, _factors_result, n
                ),
                timeout=3,
            )
            return str(pretty((await ExprConverter().convert(ctx, output))[1]))
        except asyncio.exceptions.TimeoutError:
            return "Unable to find factors in appropriate time..."

    # =========================================================================
    # =========================================================================

    @commands.command(name="factor", aliases=["factors"])
    async def _factor(
        self: typing.Self, ctx: commands.Context[TuxbotABC], n: int
    ) -> None:
        if text := await self.bot.redis.get(self.bot.utils.gen_key(n)):
            text = text.decode()
        else:
            text = await self.__factors_result(ctx, n)
            await self.bot.redis.set(self.bot.utils.gen_key(n), text)

        await ctx.send(f"```\n{text}```")
