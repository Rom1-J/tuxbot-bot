"""
tuxbot.cogs.Random.commands.Duck.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get a random picture of duck
"""
import asyncio
import typing

import aiohttp
import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from ..exceptions import APIException


class DuckCommand(commands.Cog):
    """Random duck picture"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __get_duck() -> dict[str, typing.Any]:
        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                "https://random-d.uk/api/v2/random"
            ) as s:
                if isinstance(res := await s.json(), dict):
                    return res

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        raise APIException("Something went wrong ...")

    # =========================================================================
    # =========================================================================

    @commands.command(name="duck", aliases=["randomduck"])
    async def _duck(self, ctx: commands.Context[TuxbotABC]) -> None:
        duck = await self.__get_duck()

        e = discord.Embed(
            title="Here's your duck",
            color=self.bot.utils.colors.EMBED_BORDER,
        )

        e.set_image(url=duck["url"])
        e.set_footer(text=duck["message"])

        await ctx.send(embed=e)
