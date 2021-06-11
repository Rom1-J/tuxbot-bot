import logging

import discord
from discord.ext import commands
from tuxbot.cogs.Dev.functions.HTTPs import HttpCode

from tuxbot.cogs.Dev.functions.exceptions import UnknownHttpCode

from tuxbot.cogs.Dev.functions.converters import HttpCodeConverter
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from tuxbot.core.utils.functions.extra import command_extra, ContextPlus

log = logging.getLogger("tuxbot.cogs.Dev")
_ = Translator("Dev", __file__)


class Dev(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot

    async def cog_command_error(self, ctx: ContextPlus, error):
        if isinstance(error, (UnknownHttpCode,)):
            await ctx.send(_(str(error), ctx, self.bot.config))

    # =========================================================================
    # =========================================================================

    @command_extra(name="http", deletable=True)
    async def _http(self, ctx: ContextPlus, http_code: HttpCodeConverter):
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

    # =========================================================================
