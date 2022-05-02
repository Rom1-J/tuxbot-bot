"""
tuxbot.cogs.Utils.commands.Ping.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows all pings about tuxbot
"""
import time

import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class PingCommand(commands.Cog):
    """Shows tuxbot's ping"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(name="ping")
    async def _ping(self, ctx: commands.Context):
        start = time.perf_counter()
        await ctx.typing()
        end = time.perf_counter()
        typing = round((end - start) * 1000, 2)

        start = time.perf_counter()
        await self.bot.redis.ping()
        end = time.perf_counter()
        redis = round((end - start) * 1000, 2)

        latency = round(self.bot.latency * 1000, 2)

        e = discord.Embed(title="Ping", color=discord.Color.teal())

        e.add_field(name="Websocket", value=f"{latency}ms")
        e.add_field(name="Typing", value=f"{typing}ms")
        e.add_field(name="Redis", value=f"{redis}ms")

        await ctx.send(embed=e)
