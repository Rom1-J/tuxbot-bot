"""
tuxbot.cogs.Network.commands.Dig.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows dig information from dns.bortzmeyer.org about a domain
"""

import json

import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .utils import get_from_bortzmeyer


class DigCommand(commands.Cog):
    """Shows dig information about given domain"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(name="dig")
    async def _dig(self, ctx: commands.Context, domain: str, query_type: str):
        if result := (
            await self.bot.redis.get(
                self.bot.utils.gen_key(domain, query_type)
            )
        ):
            result = json.loads(result)
        else:
            result = await get_from_bortzmeyer(domain, query_type)

            await self.bot.redis.set(
                self.bot.utils.gen_key(domain, query_type),
                json.dumps(result),
                ex=3600 * 12,
            )

        e = discord.Embed(
            title=result.get("header", f"DIG {domain} {query_type}"),
            color=0x5858D7,
        )

        if not result:
            e.add_field(
                name=f"DIG {domain} IN {query_type}",
                value="No result...",
            )
            await ctx.send(embed=e)
            return

        for i, value in enumerate(result.get("body", [])):
            e.add_field(
                name=f"#{i}",
                value=f"```{value}```",
                inline=False,
            )

        e.set_footer(text=result.get("footer"))

        await ctx.send(embed=e)
