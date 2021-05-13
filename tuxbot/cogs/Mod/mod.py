import logging

import discord
from discord.ext import commands

from tuxbot.cogs.Mod.functions.utils import save_lang
from tuxbot.core.utils import checks
from tuxbot.core.bot import Tux

from tuxbot.core.i18n import (
    Translator,
    find_locale,
    get_locale_name,
    list_locales,
)
from tuxbot.core.utils.functions.extra import (
    group_extra,
    ContextPlus,
)

log = logging.getLogger("tuxbot.cogs.Mod")
_ = Translator("Mod", __file__)


class Mod(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot

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
            await save_lang(self.bot, ctx, find_locale(lang.lower()))
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
        e = discord.Embed(
            title=_("List of available locales: ", ctx, self.bot.config),
            description=list_locales(),
            color=0x36393E,
        )

        await ctx.send(embed=e)
