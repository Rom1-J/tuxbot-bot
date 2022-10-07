"""
tuxbot.cogs.Random.commands.Panda.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get a random picture of panda
"""
import asyncio
import typing

import aiohttp
import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from ..exceptions import APIException


class PandaCommand(commands.Cog):
    """Random panda picture"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __get_panda() -> dict[str, typing.Any]:
        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                "https://some-random-api.ml/animal/panda"
            ) as s:
                if isinstance(res := await s.json(), dict):
                    return res

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        raise APIException("Something went wrong ...")

    # =========================================================================
    # =========================================================================

    @commands.command(name="panda", aliases=["randompanda"])
    async def _panda(self, ctx: commands.Context[TuxbotABC]) -> None:
        panda = await self.__get_panda()

        e = discord.Embed(
            title="Here's your panda",
            color=self.bot.utils.colors.EMBED_BORDER,
        )

        e.set_image(url=panda["image"])
        e.set_footer(text="Powered by some-random-api.ml")

        await ctx.send(embed=e)
