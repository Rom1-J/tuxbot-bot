"""
tuxbot.cogs.Logs.commands.Stats.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Send Datadog dashboard link
"""
import typing

import discord
from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.core.tuxbot import Tuxbot


class StatsCommand(commands.Cog):
    """Send Datadog dashboard link."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

        self.datadog_url = (
            "https://p.datadoghq.com/sb/"
            "9xjljtz2ur1xzb71-f2770ff41307443a259597fa4a881b0b"
        )

    # =========================================================================
    # =========================================================================

    @commands.command(name="stats", aliases=["statistics"])
    async def _stats(
        self: typing.Self, ctx: commands.Context[TuxbotABC]
    ) -> None:
        e = discord.Embed(title="Tuxbot statistics")

        e.add_field(
            name="__Datadog:__", value=f"[dashboard]({self.datadog_url})"
        )

        await ctx.send(embed=e)
