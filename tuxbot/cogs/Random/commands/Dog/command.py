"""
tuxbot.cogs.Random.commands.Dog.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Get a random picture of dog
"""
import asyncio
import typing

import aiohttp
import discord
from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.cogs.Random.commands.exceptions import APIException
from tuxbot.core.tuxbot import Tuxbot


class DogCommand(commands.Cog):
    """Random dog picture."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    async def __get_dog(self: typing.Self) -> dict[str, typing.Any]:
        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                "https://dog.ceo/api/breeds/image/random"
            ) as s:
                if isinstance(res := await s.json(), dict):
                    return res

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        msg = "Something went wrong ..."
        raise APIException(msg)

    # =========================================================================
    # =========================================================================

    @commands.command(name="dog", aliases=["randomdog"])
    async def _dog(
        self: typing.Self, ctx: commands.Context[TuxbotABC]
    ) -> None:
        dog = await self.__get_dog()

        e = discord.Embed(
            title="Here's your dog",
            color=self.bot.utils.colors.EMBED_BORDER,
        )

        e.set_image(url=dog["message"])
        e.set_footer(text="Powered by dog.ceo")

        await ctx.send(embed=e)
