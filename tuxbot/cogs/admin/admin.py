import logging

import discord
from discord.ext import commands

from tuxbot.core import checks
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator, set_locale, _locale_key_value
from tuxbot.core.utils.functions.extra import group_extra, ContextPlus

log = logging.getLogger("tuxbot.cogs.admin")
_ = Translator("Admin", __file__)


class Admin(commands.Cog, name="Admin"):
    def __init__(self, bot: Tux):
        self.bot = bot

    @group_extra(
        name="lang",
        aliases=["locale", "langue"],
        deletable=True
    )
    @commands.guild_only()
    @checks.is_admin()
    async def _lang(self, ctx: ContextPlus):
        """Manage lang settings."""

    @_lang.command(name="set", aliases=["define", "choice"])
    async def _lang_set(self, ctx: ContextPlus, lang: str):
        try:
            set_locale(lang.lower())
            await ctx.send(
                _("Locale changed to {lang} successfully")
                    .format(lang=f"`{lang}`")
            )
        except NotImplementedError:
            await ctx.send(_("This locale isn't available, execute `lang list` to view available locales"))

    @_lang.command(name="list", aliases=["liste", "all", "view"])
    async def _lang_list(self, ctx: ContextPlus):
        e = discord.Embed(
            title=_("List of available locales: "),
            description='\n'.join([i[0] for i in _locale_key_value.values()]),
            color=0x36393E
        )

        await ctx.send(embed=e)
