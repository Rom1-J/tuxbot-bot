"""
tuxbot.cogs.Random.commands.Koala.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Get a random picture of koala
"""
import asyncio
import typing

import aiohttp
import discord
from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.cogs.Random.commands.exceptions import APIException
from tuxbot.core.tuxbot import Tuxbot


class KoalaCommand(commands.Cog):
    """Random koala picture."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __get_koala() -> dict[str, typing.Any]:
        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                "https://some-random-api.ml/animal/koala"
            ) as s:
                if isinstance(res := await s.json(), dict):
                    return res

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        msg = "Something went wrong ..."
        raise APIException(msg)

    # =========================================================================
    # =========================================================================

    @commands.command(name="koala", aliases=["randomkoala"])
    async def _koala(
        self: typing.Self, ctx: commands.Context[TuxbotABC]
    ) -> None:
        koala = await self.__get_koala()

        e = discord.Embed(
            title="Here's your koala",
            color=self.bot.utils.colors.EMBED_BORDER,
        )

        e.set_image(url=koala["image"])
        e.set_footer(text="Powered by some-random-api.ml")

        await ctx.send(embed=e)
