import logging

import discord
from discord.ext import commands

from tuxbot.core import checks
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator, find_locale, get_locale_name, available_locales
from tuxbot.core.utils.functions.extra import group_extra, ContextPlus

log = logging.getLogger("tuxbot.cogs.admin")
_ = Translator("Admin", __file__)


class Admin(commands.Cog, name="Admin"):
    def __init__(self, bot: Tux):
        self.bot = bot

    async def _save_lang(self, ctx: ContextPlus, lang: str):
        await self.bot.config.update("core", f"guild.{ctx.guild.id}.locale", lang)

    @group_extra(name="lang", aliases=["locale", "langue"], deletable=True)
    @commands.guild_only()
    @checks.is_admin()
    async def _lang(self, ctx: ContextPlus):
        """Manage lang settings."""

    @_lang.command(name="set", aliases=["define", "choice"])
    async def _lang_set(self, ctx: ContextPlus, lang: str):
        try:
            await self._save_lang(ctx, find_locale(lang.lower()))
            await ctx.send(
                _("Locale changed to {lang} successfully", ctx, self.bot.config).format(
                    lang=f"`{get_locale_name(lang).lower()}`"
                )
            )
        except NotImplementedError:
            await self._lang_list(ctx)

    @_lang.command(name="list", aliases=["liste", "all", "view"])
    async def _lang_list(self, ctx: ContextPlus):
        e = discord.Embed(
            title=_("List of available locales: ", ctx, self.bot.config),
            description="\n".join([i[0] for i in available_locales.values()]),
            color=0x36393E,
        )

        await ctx.send(embed=e)
