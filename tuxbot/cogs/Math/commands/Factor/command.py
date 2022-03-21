"""
tuxbot.cogs.Math.commands.factor.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decompose given number in prime factors
"""
import asyncio

from discord.ext import commands
from sympy import factorint, pretty

from tuxbot.core.Tuxbot import Tuxbot

from ...converters.ExprConverter import ExprConverter


class FactorCommand(commands.Cog):
    """Decompose in prime factors"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __factors_result(ctx: commands.Context, n: int) -> str:
        """Generate prime factor decomposition of n"""

        def _factors_result(_n: int) -> str:
            return " + ".join(
                    [f"{k}**{v}" for k, v in factorint(_n).items()]
                )
        try:
            output = await asyncio.wait_for(
                asyncio.get_running_loop().run_in_executor(
                    None, _factors_result, n
                ),
                timeout=3,
            )
            return pretty((await ExprConverter().convert(ctx, output))[1])
        except asyncio.exceptions.TimeoutError:
            return "Unable to find factors in appropriate time..."

    # =========================================================================
    # =========================================================================

    @commands.command(name="factor", aliases=["factors"])
    async def _factor(self, ctx: commands.Context, n: int):
        if text := await self.bot.redis.get(self.bot.utils.gen_key(n)):
            text = text.decode()
        else:
            text = await self.__factors_result(ctx, n)
            await self.bot.redis.set(self.bot.utils.gen_key(n), text)

        await ctx.send(f"```\n{text}```")
