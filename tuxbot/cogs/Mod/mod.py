import logging
from datetime import datetime
from typing import Optional

import discord
from discord.ext import commands

from tuxbot.cogs.Mod.functions import listeners
from tuxbot.cogs.Mod.functions.converters import (
    RuleConverter,
    RuleIDConverter,
    BotMessageConverter,
    ReasonConverter,
    AutoBanConverter,
)
from tuxbot.cogs.Mod.functions.exceptions import (
    RuleTooLongException,
    UnknownRuleException,
    NonMessageException,
    NonBotMessageException,
    ReasonTooLongException,
)
from tuxbot.cogs.Mod.functions.utils import (
    save_lang,
    get_server_rules,
    format_rule,
    get_most_recent_server_rules,
    paginate_server_rules,
    get_mute_role,
    create_mute_role,
)
from tuxbot.cogs.Mod.models import AutoBan
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
    command_extra,
)

log = logging.getLogger("tuxbot.cogs.Mod")
_ = Translator("Mod", __file__)


class Mod(commands.Cog):
    def __init__(self, bot: Tux, version_info):
        self.bot = bot
        self.version_info = version_info

    async def cog_command_error(self, ctx: ContextPlus, error):
        if isinstance(
            error,
            (
                RuleTooLongException,
                UnknownRuleException,
                NonMessageException,
                NonBotMessageException,
                ReasonTooLongException,
            ),
        ):
            return await ctx.send(_(str(error), ctx, self.bot.config))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await listeners.on_member_join(self, member)

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

        if not rules:
            return await ctx.send(
                _("No rules found for this server", ctx, self.bot.config)
            )

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

        rule_row.rule_id = (
            len(await get_server_rules(ctx.guild.id)) + 1  # type: ignore
        )
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

    @checks.is_admin()
    @_rule.command(name="update")
    async def _rule_update(
        self,
        ctx: ContextPlus,
        message: BotMessageConverter,
    ):
        rules = await get_server_rules(ctx.guild.id)

        if not rules:
            return await ctx.send(
                _("No rules found for this server", ctx, self.bot.config)
            )

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

        # noinspection PyTypeChecker
        to_edit: discord.Message = message

        if len(pages) == 1:
            embed.description = pages[0]

            await to_edit.edit(content="", embed=embed)
        else:
            for i, page in enumerate(pages):
                embed.title = _(
                    "Rules for {} ({}/{})", ctx, self.bot.config
                ).format(ctx.guild.name, str(i + 1), str(len(pages)))
                embed.description = page

                await to_edit.edit(content="", embed=embed)

    # =========================================================================

    @group_extra(
        name="mute",
        deletable=True,
        invoke_without_command=True,
    )
    @commands.guild_only()
    @checks.is_admin()
    async def _mute(
        self,
        ctx: ContextPlus,
        members: commands.Greedy[discord.Member],
        *,
        reason: Optional[ReasonConverter],
    ):
        if not members:
            return await ctx.send(_("Missing members", ctx, self.bot.config))

        role_row = await get_mute_role(ctx.guild.id)

        if role_row is None:
            return await ctx.send(
                _(
                    "No mute role has been specified for this guild",
                    ctx,
                    self.bot.config,
                )
            )

        for member in members:
            await member.add_roles(
                discord.Object(id=int(role_row.role_id)), reason=reason
            )

        await ctx.send("\N{THUMBS UP SIGN}")

    @_mute.command(name="show", aliases=["role"])
    async def _mute_show(
        self,
        ctx: ContextPlus,
    ):
        role_row = await get_mute_role(ctx.guild.id)

        if (
            role_row is None
            or (role := ctx.guild.get_role(int(role_row.role_id))) is None
        ):
            return await ctx.send(
                _(
                    "No mute role has been specified for this guild",
                    ctx,
                    self.bot.config,
                )
            )

        muted_members = [m for m in ctx.guild.members if role in m.roles]

        e = discord.Embed(
            title=f"Role: {role.name} (ID: {role.id})", color=role.color
        )
        e.add_field(name="Total mute:", value=len(muted_members))

        await ctx.send(embed=e)

    @_mute.command(name="set", aliases=["define"])
    async def _mute_set(self, ctx: ContextPlus, role: discord.Role):
        role_row = await get_mute_role(ctx.guild.id)

        if role_row is None:
            await create_mute_role(ctx.guild.id, role.id)
        else:
            role_row.role_id = role.id  # type: ignore
            await role_row.save()

        await ctx.send(
            _("Mute role successfully defined", ctx, self.bot.config)
        )

    # =========================================================================

    @command_extra(
        name="tempmute",
        deletable=True,
    )
    @commands.guild_only()
    @checks.is_admin()
    async def _tempmute(
        self,
        ctx: ContextPlus,
        time,
        members: discord.Member,
        *,
        reason: Optional[ReasonConverter],
    ):
        _, _, _, _ = ctx, time, members, reason

    # =========================================================================

    @command_extra(
        name="unmute",
        deletable=True,
    )
    @commands.guild_only()
    @checks.is_admin()
    async def _unmute(
        self,
        ctx: ContextPlus,
        members: commands.Greedy[discord.Member],
        *,
        reason: Optional[ReasonConverter],
    ):
        if not members:
            return await ctx.send(_("Missing members", ctx, self.bot.config))

        role_row = await get_mute_role(ctx.guild.id)

        if role_row is None:
            return await ctx.send(
                _(
                    "No mute role has been specified for this guild",
                    ctx,
                    self.bot.config,
                )
            )

        for member in members:
            await member.remove_roles(
                discord.Object(id=int(role_row.role_id)), reason=reason
            )

        await ctx.send("\N{THUMBS UP SIGN}")

    # =========================================================================

    # noinspection PyUnresolvedReferences
    @command_extra(
        name="autoban",
        deletable=True,
    )
    @commands.guild_only()
    @checks.is_admin()
    async def _autoban(
        self,
        ctx: ContextPlus,
        *,
        args: AutoBanConverter,
    ):
        if args is None:
            return await ctx.send(
                _("Unable to parse arguments", ctx, self.bot.config)
            )

        if args.delete:
            autoban_row = await AutoBan.get_or_none(
                server_id=ctx.guild.id, match=args.match
            )

            if autoban_row is None:
                return await ctx.send(
                    _("Unable to find this match", ctx, self.bot.config)
                )

            await autoban_row.delete()
        else:
            autoban_row = await AutoBan()

            autoban_row.server_id = ctx.guild.id
            autoban_row.match = args.match
            autoban_row.reason = args.reason
            autoban_row.log_channel = args.log_channel

            await autoban_row.save()

        await ctx.send("\N{THUMBS UP SIGN}")
