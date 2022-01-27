"""
tuxbot.cogs.Network.commands.Getheaders.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shows address headers.
"""

import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .utils import check_for_rfc1918_or_raise, get_headers


class GetheadersCommand(commands.Cog):
    """Shows address headers"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command(name="getheaders", aliases=["headers"])
    async def _getheaders(
        self, ctx: commands.Context, ip: str, *, user_agent: str = ""
    ):
        if not ip.startswith("http"):
            ip = f"http://{ip}"

        await check_for_rfc1918_or_raise(ip)

        session, headers = await get_headers(ip, user_agent)
        colors = {
            "1": 0x17A2B8,
            "2": 0x28A745,
            "3": 0xFFC107,
            "4": 0xDC3545,
            "5": 0x343A40,
        }

        e = discord.Embed(
            title=f"Headers : {ip}",
            color=colors.get(str(session.status)[0], 0x6C757D),
        )
        e.add_field(
            name="Status", value=f"```{session.status}```", inline=True
        )
        e.set_thumbnail(url=f"https://http.cat/{session.status}")

        for key, value in headers.items():
            _, output = await self.bot.utils.shorten(value, 50)

            if output["link"]:
                value = f"[show all]({output['link']})"
            else:
                value = f"```\n{output['text']}```"

            e.add_field(name=key, value=value, inline=True)

        await ctx.send(embed=e)
