"""
tuxbot.cogs.Network.commands.Dig.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows dig information from dns.bortzmeyer.org about a domain
"""
import asyncio
import json
from typing import Any

import aiohttp
import discord
from bs4 import BeautifulSoup
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class DigCommand(commands.Cog):
    """Shows dig information about given domain"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @staticmethod
    def __parse_from_bortzmeyer(html: str) -> dict[str, Any]:
        """Parse HTML result as dict object"""

        soup = BeautifulSoup(html, "html.parser")

        body = soup.find(class_="body")

        try:
            return {
                "header": soup.find(name="h1").text,
                "body": list(map(lambda el: el.text, body.select("li>span"))),
                "footer": body.find(name="p").text,
            }
        except AttributeError:
            return {}

    # =========================================================================

    async def __get_from_bortzmeyer(
        self, domain: str, query_type: str
    ) -> dict[str, Any]:
        """Get result from https://dns.bortzmeyer.org/"""

        try:
            async with aiohttp.ClientSession() as cs, cs.get(
                f"https://dns.bortzmeyer.org/{domain}/{query_type}",
                timeout=aiohttp.ClientTimeout(total=2),
            ) as s:
                return self.__parse_from_bortzmeyer(await s.text())
        except (aiohttp.ClientError, asyncio.exceptions.TimeoutError):
            pass

        return {}

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
            result = await self.__get_from_bortzmeyer(domain, query_type)

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
