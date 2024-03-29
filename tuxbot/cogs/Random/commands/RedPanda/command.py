"""
tuxbot.cogs.Random.commands.RedPanda.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get a random picture of red panda
"""
import asyncio
import typing

import aiohttp
import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from ..exceptions import APIException


class RedPandaCommand(commands.Cog):
    """Random red panda picture"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __get_redpanda() -> dict[str, typing.Any]:
        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                "https://some-random-api.ml/animal/red_panda"
            ) as s:
                if isinstance(res := await s.json(), dict):
                    return res

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        raise APIException("Something went wrong ...")

    # =========================================================================
    # =========================================================================

    @commands.command(name="redpanda", aliases=["randomredpanda"])
    async def _redpanda(self, ctx: commands.Context[TuxbotABC]) -> None:
        redpanda = await self.__get_redpanda()

        e = discord.Embed(
            title="Here's your red panda",
            color=self.bot.utils.colors.EMBED_BORDER,
        )

        e.set_image(url=redpanda["image"])
        e.set_footer(text="Powered by some-random-api.ml")

        await ctx.send(embed=e)
