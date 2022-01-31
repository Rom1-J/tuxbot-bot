"""
tuxbot.cogs.Dev.commands.HTTP.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command to show doc about HTTP code
"""

import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .converters.HttpCodeConverter import HttpCodeConverter
from .HTTPs import HttpCode


class HTTPCommand(commands.Cog):
    """Shows HTTP code doc"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.command(name="http")
    async def _http(self, ctx: commands.Context, http_code: HttpCodeConverter):
        if isinstance(http_code, HttpCode):
            e = discord.Embed(
                title=f"{http_code.value} {http_code.name}", color=0x2F3136
            )

            if http_code.cat:
                e.set_image(url=f"https://http.cat/{http_code.value}")

            if http_code.mdn:
                url = (
                    "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status"
                    f"/{http_code.value}"
                )
                e.add_field(name="MDN", value=f"> [{url}]({url})")
                e.set_image(url=f"https://http.cat/{http_code.value}")

            await ctx.send(embed=e)
