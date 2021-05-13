import logging
from datetime import datetime

import discord
from discord.ext import commands

from tuxbot.cogs.Mod.functions.converters import RuleConverter, RuleIDConverter
from tuxbot.cogs.Mod.functions.exceptions import (
    RuleTooLongException,
    UnknownRuleException,
)
from tuxbot.cogs.Mod.functions.utils import (
    save_lang,
    get_server_rules,
    format_rule,
    get_most_recent_server_rules,
    paginate_server_rules,
)
from tuxbot.cogs.Mod.models.rules import Rule
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

    async def cog_command_error(self, ctx: ContextPlus, error):
        if isinstance(
            error,
            (
                RuleTooLongException,
                UnknownRuleException,
            ),
        ):
            await ctx.send(_(str(error), ctx, self.bot.config))

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

    # =========================================================================

    @group_extra(
        name="rule",
        aliases=["rules", "regle", "regles"],
        deletable=False,
        invoke_without_command=True,
    )
    @commands.guild_only()
    async def _rule(
        self,
        ctx: ContextPlus,
        rule: RuleIDConverter,
        members: commands.Greedy[discord.Member],
    ):
        rule_row = await Rule.get(server_id=ctx.guild.id, rule_id=rule)

        message = _(
            "{}please read the following rule: \n{}", ctx, self.bot.config
        )
        authors = ""

        for member in members:
            if member in ctx.message.mentions:
                authors += f"{member.name}#{member.discriminator}, "
            else:
                authors += f"{member.mention}, "

        await ctx.send(message.format(authors, format_rule(rule_row)))

    @_rule.command(name="list", aliases=["show", "all"])
    async def _rule_list(self, ctx: ContextPlus):
        rules = await get_server_rules(ctx.guild.id)

        embed = discord.Embed(
            title=_("Rules for {}", ctx, self.bot.config).format(
                ctx.guild.name
            ),
            color=discord.Color.blue(),
        )
        embed.set_footer(
            text=_("Latest change: {}", ctx, self.bot.config).format(
                get_most_recent_server_rules(rules).updated_at.ctime()
            )
        )

        pages = paginate_server_rules(rules)

        if len(pages) == 1:
            embed.description = pages[0]

            await ctx.send(embed=embed)
        else:
            for i, page in enumerate(pages):
                embed.title = _(
                    "Rules for {} ({}/{})", ctx, self.bot.config
                ).format(ctx.guild.name, str(i + 1), str(len(pages)))
                embed.description = page

                await ctx.send(embed=embed)

    @checks.is_admin()
    @_rule.command(name="add")
    async def _rule_add(self, ctx: ContextPlus, *, rule: RuleConverter):
        rule_row = await Rule()
        rule_row.server_id = ctx.guild.id
        rule_row.author_id = ctx.message.author.id

        rule_row.rule_id = len(await get_server_rules(ctx.guild.id)) + 1  # type: ignore
        rule_row.content = str(rule)  # type: ignore

        await rule_row.save()

        await ctx.send(
            _("Following rule added: \n{}", ctx, self.bot.config).format(
                format_rule(rule_row)
            )
        )

    @checks.is_admin()
    @_rule.command(name="edit")
    async def _rule_edit(
        self,
        ctx: ContextPlus,
        rule: RuleIDConverter,
        *,
        content: RuleConverter,
    ):
        # noinspection PyTypeChecker
        rule_row = await Rule.get(server_id=ctx.guild.id, rule_id=rule)

        rule_row.content = str(content)  # type: ignore
        rule_row.updated_at = datetime.now()  # type: ignore

        await rule_row.save()

        await ctx.send(
            _("Following rule updated: \n{}", ctx, self.bot.config).format(
                format_rule(rule_row)
            )
        )

    @checks.is_admin()
    @_rule.command(name="delete")
    async def _rule_delete(
        self,
        ctx: ContextPlus,
        rule: RuleIDConverter,
    ):
        # noinspection PyTypeChecker
        rule_row = await Rule.get(server_id=ctx.guild.id, rule_id=rule)

        await rule_row.delete()

        await ctx.send(
            _("Following rule deleted: \n{}", ctx, self.bot.config).format(
                format_rule(rule_row)
            )
        )
