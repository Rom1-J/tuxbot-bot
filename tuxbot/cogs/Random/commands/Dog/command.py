"""
tuxbot.cogs.Random.commands.Dog.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get a random picture of dog
"""
import asyncio

import aiohttp
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from ..exceptions import APIException


class DogCommand(commands.Cog):
    """Random dog picture"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    async def __get_dog(self) -> dict:
        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                "https://dog.ceo/api/breeds/image/random"
            ) as s:
                return await s.json()

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        raise APIException("Something went wrong ...")

    # =========================================================================
    # =========================================================================

    @commands.command(name="dog", aliases=["randomdog"])
    async def _dog(self, ctx: commands.Context):
        dog = await self.__get_dog()

        e = discord.Embed(
            title="Here's your dog",
            color=self.bot.utils.colors.EMBED_BORDER.value,
        )

        e.set_image(url=dog["message"])
        e.set_footer(text="Powered by dog.ceo")

        await ctx.send(embed=e)
