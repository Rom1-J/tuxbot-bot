import inspect
import logging
import os
import platform
from typing import Optional

import discord
import humanize
import psutil
from discord.ext import commands
from tuxbot.cogs.Utils.functions.quote import Quote

from tuxbot import version_info as tuxbot_version_info, __version__

from tuxbot.core.utils.functions.extra import command_extra, ContextPlus
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import Translator
from .functions.converters import QuoteConverter, UserOrMeConverter
from .functions.exceptions import UserNotFound
from .functions.info import fetch_info

log = logging.getLogger("tuxbot.cogs.Utils")
_ = Translator("Utils", __file__)


class Utils(commands.Cog):
    def __init__(self, bot: Tux, version_info):
        self.bot = bot
        self.version_info = version_info

    # =========================================================================

    async def cog_command_error(self, ctx: ContextPlus, error):
        if isinstance(error, UserNotFound):
            await ctx.send(_(str(error), ctx, self.bot.config))

    # =========================================================================
    # =========================================================================

    @command_extra(name="info", aliases=["about"])
    async def _info(self, ctx: ContextPlus):
        proc = psutil.Process()
        infos = await fetch_info()

        with proc.oneshot():
            mem = proc.memory_full_info()
            cpu = proc.cpu_percent() / psutil.cpu_count()

            e = discord.Embed(
                title=_("Information about TuxBot", ctx, self.bot.config),
                color=0x89C4F9,
            )

            e.add_field(
                name=_(
                    "__:busts_in_silhouette: Development__",
                    ctx,
                    self.bot.config,
                ),
                value="**Romain#5117:** [git](https://github.com/Rom1-J)\n"
                "**Outout#4039:** [git](https://git.gnous.eu/mael)\n",
                inline=True,
            )
            e.add_field(
                name="__<:python:596577462335307777> Python__",
                value=f"**python** `{platform.python_version()}`\n"
                f"**discord.py** `{discord.__version__}`",
                inline=True,
            )
            e.add_field(
                name="__:gear: Usage__",
                value=_(
                    "**{}** physical memory\n"
                    "**{}** virtual memory\n"
                    "**{:.2f}**% CPU",
                    ctx,
                    self.bot.config,
                ).format(
                    humanize.naturalsize(mem.rss),
                    humanize.naturalsize(mem.vms),
                    cpu,
                ),
                inline=True,
            )

            e.add_field(
                name=_("__Servers count__", ctx, self.bot.config),
                value=str(len(self.bot.guilds)),
                inline=True,
            )
            e.add_field(
                name=_("__Channels count__", ctx, self.bot.config),
                value=str(len(list(self.bot.get_all_channels()))),
                inline=True,
            )
            e.add_field(
                name=_("__Members count__", ctx, self.bot.config),
                value=str(len(list(self.bot.get_all_members()))),
                inline=True,
            )

            e.add_field(
                name=_("__:file_folder: Files__", ctx, self.bot.config),
                value=f"{infos.get('file_amount')} "
                f"*({infos.get('python_file_amount')}"
                f" <:python:596577462335307777>)*",
                inline=True,
            )
            e.add_field(
                name=_("__¶ Lines__", ctx, self.bot.config),
                value=f"{infos.get('total_lines')} "
                f"*({infos.get('total_python_class')} "
                + _("class", ctx, self.bot.config)
                + ","
                f" {infos.get('total_python_functions')} "
                + _("functions", ctx, self.bot.config)
                + ","
                f" {infos.get('total_python_coroutines')} "
                + _("coroutines", ctx, self.bot.config)
                + ","
                f" {infos.get('total_python_comments')} "
                + _("comments", ctx, self.bot.config)
                + ")*",
                inline=True,
            )

            e.add_field(
                name=_("__Latest changes__", ctx, self.bot.config),
                value=tuxbot_version_info.info,
                inline=False,
            )

            e.add_field(
                name=_("__:link: Links__", ctx, self.bot.config),
                value="[tuxbot.gnous.eu](https://tuxbot.gnous.eu/) "
                "| [gnous.eu](https://gnous.eu/) "
                "| [git](https://gitlab.gnous.eu/gnouseu/tuxbot-bot) "
                "| [status](https://status.gnous.eu/check/154250) "
                + _("| [Invite]", ctx, self.bot.config)
                + "(https://discordapp.com/oauth2/authorize?client_id="
                "301062143942590465&scope=bot&permissions=268749888)",
                inline=False,
            )

            e.set_footer(text=f"version: {__version__} • prefix: {ctx.prefix}")

        await ctx.send(embed=e)

    # =========================================================================

    @command_extra(name="credits", aliases=["contributors", "authors"])
    async def _credits(self, ctx: ContextPlus):
        e = discord.Embed(
            title=_("Contributors", ctx, self.bot.config), color=0x2F3136
        )

        e.add_field(
            name="**Romain#5117** ",
            value="> • [github](https://github.com/Rom1-J)\n"
            "> • [gitlab](https://gitlab.gnous.eu/Romain)\n"
            "> • romain@gnous.eu",
            inline=True,
        )
        e.add_field(
            name="**Outout#4039** ",
            value="> • [gitea](https://git.gnous.eu/mael)\n"
            "> • [@outoutxyz](https://twitter.com/outouxyz)\n"
            "> • mael@gnous.eu",
            inline=True,
        )

        await ctx.send(embed=e)

    # =========================================================================

    @command_extra(name="invite")
    async def _invite(self, ctx: ContextPlus):
        basic_perms = discord.Permissions(
            add_reactions=True,
            read_messages=True,
            send_messages=True,
            manage_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            external_emojis=True,
            connect=True,
            speak=True,
            manage_roles=True,
        )

        admin_perms = discord.Permissions(
            create_instant_invite=True,
            kick_members=True,
            ban_members=True,
            add_reactions=True,
            read_messages=True,
            send_messages=True,
            manage_messages=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            external_emojis=True,
            connect=True,
            speak=True,
            manage_roles=True,
        )

        e = discord.Embed(
            title=_("Invite", ctx, self.bot.config), color=0x2F3136
        )

        e.add_field(
            name=_("Minimal", ctx, self.bot.config),
            value=_(
                "The minimum permissions include the strict requirements for "
                "the proper functioning of all basics commands.\n",
                ctx,
                self.bot.config,
            )
            + _("[Add!]", ctx, self.bot.config)
            + f"({discord.utils.oauth_url(self.bot.user.id, permissions=basic_perms)})",
            inline=False,
        )
        e.add_field(
            name=_("Admin", ctx, self.bot.config),
            value=_(
                "All minimal permissions + extra permissions for admin "
                "commands such as kick and ban\n",
                ctx,
                self.bot.config,
            )
            + _("[Add!]", ctx, self.bot.config)
            + f"({discord.utils.oauth_url(self.bot.user.id, permissions=admin_perms)})",
            inline=False,
        )

        await ctx.send(embed=e)

    # =========================================================================

    @command_extra(name="source")
    async def _source(self, ctx: ContextPlus, *, name=None):
        base_url = "https://github.com/Rom1-J/tuxbot-bot"

        if not name:
            return await ctx.send(f"<{base_url}>")

        cmd = self.bot.get_command(name)

        if cmd:
            # noinspection PyUnresolvedReferences
            src = cmd.callback.__code__
            rpath = src.co_filename
        else:
            return await ctx.send(
                _("Unable to find `{}`", ctx, self.bot.config).format(name)
            )

        try:
            lines, start_line = inspect.getsourcelines(src)
        except OSError:
            return await ctx.send(
                _(
                    "Unable to fetch lines for `{}`", ctx, self.bot.config
                ).format(name)
            )

        location = (
            os.path.relpath(rpath)
            .replace("\\", "/")
            .split("site-packages/")[1]
        )

        final_url = (
            f"<{base_url}/tree/master/{location}#L{start_line}"
            f"-L{start_line + len(lines) - 1}>"
        )
        await ctx.send(final_url)

    # =========================================================================

    @command_extra(name="quote")
    async def _quote(self, ctx: ContextPlus, *, message: QuoteConverter):
        # noinspection PyUnresolvedReferences
        quote = Quote(self.bot.loop, message.content, str(message.author))

        quote_bytes = await quote.generate()
        file = discord.File(quote_bytes, "quote.png")

        await ctx.send(file=file)

    # =========================================================================

    @command_extra(name="ui", aliases=["user_info", "userinfo"])
    async def _ui(
        self, ctx: ContextPlus, *, user_id: Optional[UserOrMeConverter] = None
    ):
        user_id = user_id or ctx.author

        e = discord.Embed(color=self.bot.colors.EMBED_BORDER.value)

        if isinstance(user_id, (discord.User, discord.Member)):
            e.set_author(name=user_id, icon_url=user_id.display_avatar.url)
            e.set_thumbnail(url=user_id.display_avatar.url)
            e.set_footer(text=f"ID: {user_id.id}")

            e.add_field(
                name=_("Created at", ctx, self.bot.config),
                value=f"> <t:{int(user_id.created_at.timestamp())}:F>",
                inline=True,
            )

        if isinstance(user_id, discord.Member):
            e.add_field(
                name=_("Joined at", ctx, self.bot.config),
                value=f"> <t:{int(user_id.joined_at.timestamp())}:F>",
                inline=True,
            )

            if roles := user_id.roles[1:]:
                e.add_field(
                    name=f"Roles ({len(roles)})",
                    value=" ".join(role.mention for role in roles),
                    inline=False,
                )

            if premium_since := user_id.premium_since:
                e.add_field(
                    name=_("Premium since", ctx, self.bot.config),
                    value=f"> <t:{int(premium_since.timestamp())}:F>",
                )

            # noinspection PyUnresolvedReferences
            if (
                status := user_id.status.value.upper()
            ) in self.bot.colors.__members__:
                e.colour = getattr(self.bot.colors, status).value

            if activity := user_id.activity:
                e.description = activity.name

        await ctx.send(embed=e)
