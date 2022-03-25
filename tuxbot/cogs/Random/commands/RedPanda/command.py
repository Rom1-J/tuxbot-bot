"""
tuxbot.cogs.Random.commands.RedPanda.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get a random picture of red panda
"""
import asyncio

import aiohttp
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from ..exceptions import APIException


class RedPandaCommand(commands.Cog):
    """Random red panda picture"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __get_redpanda() -> dict:
        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                "https://some-random-api.ml/animal/red_panda"
            ) as s:
                return await s.json()

        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        raise APIException("Something went wrong ...")

    # =========================================================================
    # =========================================================================

    @commands.command(name="redpanda", aliases=["randomredpanda"])
    async def _redpanda(self, ctx: commands.Context):
        redpanda = await self.__get_redpanda()

        e = discord.Embed(
            title="Here's your red panda",
            color=self.bot.utils.colors.EMBED_BORDER.value,
        )

        e.set_image(url=redpanda["image"])
        e.set_footer(text="Powered by some-random-api.ml")

        await ctx.send(embed=e)
