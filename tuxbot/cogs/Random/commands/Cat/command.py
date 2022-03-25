"""
tuxbot.cogs.Random.commands.Cat.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get a random picture of cat
"""
import asyncio
import random

import aiohttp
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .exceptions import CATAASException


class CatCommand(commands.Cog):
    """Random cat picture"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        self.cataas_url = (
            "https://cataas.com"
        )

    # =========================================================================
    # =========================================================================

    async def __get_cat(self) -> dict:
        try:
            endpoint = random.choices(
                ['cat', 'cat/gif'],
                weights=[0.8, 0.2],
                k=1
            )[0]

            async with aiohttp.ClientSession() as cs, cs.get(
                f"{self.cataas_url}/{endpoint}?json=true"
            ) as s:
                return await s.json()

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        raise CATAASException("Something went wrong ...")

    # =========================================================================
    # =========================================================================

    @commands.command(name="cat", aliases=["randomcat"])
    async def _cat(self, ctx: commands.Context):
        cat = await self.__get_cat()

        e = discord.Embed(
            title="Here's your cat",
            color=self.bot.utils.colors.EMBED_BORDER.value,
        )

        e.set_image(url=f"{self.cataas_url}/{cat['url']}")
        e.set_footer(text="Powered by cataas.com")

        await ctx.send(embed=e)
