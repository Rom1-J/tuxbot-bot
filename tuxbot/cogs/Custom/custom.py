import logging
from typing import List

import discord
from discord.ext import commands

from tuxbot.cogs.Custom.functions.converters import AliasConvertor
from tuxbot.core.bot import Tux
from tuxbot.core.config import set_for_key, search_for, set_if_none
from tuxbot.core.config import Config
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

log = logging.getLogger("tuxbot.cogs.Custom")
_ = Translator("Custom", __file__)


class Custom(commands.Cog):
    def __init__(self, bot: Tux):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(_(str(error), ctx, self.bot.config))

    # =========================================================================
    # =========================================================================

    async def _get_aliases(self, ctx: ContextPlus) -> dict:
        return search_for(self.bot.config.Users, ctx.author.id, "aliases")

    async def _save_lang(self, ctx: ContextPlus, lang: str) -> None:
        set_for_key(
            self.bot.config.Users, ctx.author.id, Config.User, locale=lang
        )

    async def _save_alias(self, ctx: ContextPlus, alias: dict) -> None:
        set_for_key(
            self.bot.config.Users, ctx.author.id, Config.User, alias=alias
        )

    # =========================================================================
    # =========================================================================

    @group_extra(name="custom", aliases=["perso"], deletable=True)
    @commands.guild_only()
    async def _custom(self, ctx: ContextPlus):
        """Manage custom settings."""

    @_custom.command(name="locale", aliases=["langue", "lang"])
    async def _custom_locale(self, ctx: ContextPlus, lang: str):
        try:
            await self._save_lang(ctx, find_locale(lang.lower()))
            await ctx.send(
                _(
                    "Locale changed for you to {lang} successfully",
                    ctx,
                    self.bot.config,
                ).format(lang=f"`{get_locale_name(lang).lower()}`")
            )
        except NotImplementedError:
            e = discord.Embed(
                title=_("List of available locales: ", ctx, self.bot.config),
                description=list_locales,
                color=0x36393E,
            )

            await ctx.send(embed=e)

    @_custom.command(name="alias", aliases=["aliases"])
    async def _custom_alias(self, ctx: ContextPlus, *, alias: AliasConvertor):
        args: List[str] = str(alias).split(" | ")

        command = args[0]
        custom = args[1]

        user_aliases = await self._get_aliases(ctx)

        if not user_aliases:
            set_if_none(self.bot.config.Users, ctx.author.id, Config.User)
            user_aliases = await self._get_aliases(ctx)

        if custom in user_aliases.keys():
            return await ctx.send(
                _(
                    "The alias `{alias}` is already defined "
                    "for the command `{command}`",
                    ctx,
                    self.bot.config,
                ).format(alias=custom, command=user_aliases.get(custom))
            )

        user_aliases[custom] = command

        await self._save_alias(ctx, user_aliases)

        await ctx.send(
            _(
                "The alias `{alias}` for the command `{command}` "
                "was successfully created",
                ctx,
                self.bot.config,
            ).format(alias=custom, command=command)
        )
