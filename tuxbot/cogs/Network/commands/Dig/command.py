"""
tuxbot.cogs.Network.commands.Dig.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows dig information from dns.bortzmeyer.org about a domain
"""

import json

import discord
from discord.ext import commands

from tuxbot.cogs.Network.commands.Dig.utils import get_from_bortzmeyer
from tuxbot.core.Tuxbot import Tuxbot


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

        e = discord.Embed(title=f"DIG {domain} {query_type}", color=0x5858D7)

        if not result or not result.get("AnswerSection"):
            e.add_field(
                name=f"DIG {domain} IN {query_type}",
                value="No result...",
            )
            await ctx.send(embed=e)
            return

        for i, value in enumerate(result["AnswerSection"]):
            data = (
                value.get("Text")
                or value.get("Address")
                or value.get("MailExchanger")
                or value.get("Target")
                or f"{value.get('MasterServerName', '')}"
                f" {value.get('MaintainerName', '')}".strip()
            )
            e.add_field(
                name=f"#{i}",
                value=f"```{value.get('Name')} "
                f"{value.get('TTL')} "
                f"{result['QuestionSection'].get('Qclass')} "
                f"{value.get('Type')} "
                f"{data}```",
                inline=False,
            )

        await ctx.send(embed=e)
