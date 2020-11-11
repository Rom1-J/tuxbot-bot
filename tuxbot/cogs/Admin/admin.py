import logging

import discord
from discord.ext import commands

from tuxbot.core.utils import checks
from tuxbot.core.bot import Tux
from tuxbot.core.config import set_for_key
from tuxbot.core.config import Config
from tuxbot.core.i18n import (
    Translator,
    find_locale,
    get_locale_name,
    available_locales,
)
from tuxbot.core.utils.functions.extra import (
    group_extra,
    command_extra,
    ContextPlus,
)

log = logging.getLogger("tuxbot.cogs.Admin")
_ = Translator("Admin", __file__)


class Admin(commands.Cog, name="Admin"):
    def __init__(self, bot: Tux):
        self.bot = bot

    async def _save_lang(self, ctx: ContextPlus, lang: str):
        set_for_key(
            self.bot.config.Servers, ctx.guild.id, Config.Server, locale=lang
        )

    # =========================================================================
    # =========================================================================

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
                _(
                    "Locale changed to {lang} successfully",
                    ctx,
                    self.bot.config,
                ).format(lang=f"`{get_locale_name(lang).lower()}`")
            )
        except NotImplementedError:
            await self._lang_list(ctx)

    @_lang.command(name="list", aliases=["liste", "all", "view"])
    async def _lang_list(self, ctx: ContextPlus):
        description = ""
        for key, value in available_locales.items():
            description += f":flag_{key[-2:].lower()}: {value[0]}\n"

        e = discord.Embed(
            title=_("List of available locales: ", ctx, self.bot.config),
            description=description,
            color=0x36393E,
        )

        await ctx.send(embed=e)

    # =========================================================================

    @command_extra(name="quit", aliases=["shutdown"], deletable=False)
    @commands.guild_only()
    @checks.is_owner()
    async def _quit(self, ctx: ContextPlus):
        await ctx.send("*quit...*")
        await self.bot.shutdown()

    @command_extra(name="restart", deletable=False)
    @commands.guild_only()
    @checks.is_owner()
    async def _restart(self, ctx: ContextPlus):
        await ctx.send("*restart...*")
        await self.bot.shutdown(restart=True)
