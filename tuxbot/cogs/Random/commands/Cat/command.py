"""
tuxbot.cogs.Random.commands.Cat.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get a random picture of cat
"""
import asyncio
import random
import typing

import aiohttp
import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from ..exceptions import APIException


class CatCommand(commands.Cog):
    """Random cat picture"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        self.cataas_url = "https://cataas.com"

    # =========================================================================
    # =========================================================================

    async def __get_cat(self) -> dict[str, typing.Any]:
        try:
            endpoint = random.choices(
                ["cat", "cat/gif"], weights=[0.8, 0.2], k=1
            )[0]

            async with aiohttp.ClientSession() as cs, cs.get(
                f"{self.cataas_url}/{endpoint}?json=true"
            ) as s:
                if isinstance(res := await s.json(), dict):
                    return res

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        raise APIException("Something went wrong ...")

    # =========================================================================
    # =========================================================================

    @commands.command(name="cat", aliases=["randomcat"])
    async def _cat(self, ctx: commands.Context[TuxbotABC]) -> None:
        cat = await self.__get_cat()

        e = discord.Embed(
            title="Here's your cat",
            color=self.bot.utils.colors.EMBED_BORDER,
        )

        e.set_image(url=f"{self.cataas_url}/{cat['url']}")
        e.set_footer(text="Powered by cataas.com")

        await ctx.send(embed=e)
