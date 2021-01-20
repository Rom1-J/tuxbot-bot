import inspect
import logging
import os
import platform

import discord
import humanize
import psutil
from discord.ext import commands
from tuxbot import version_info, __version__

from tuxbot.core.utils.functions.extra import command_extra, ContextPlus
from tuxbot.core.bot import Tux
from tuxbot.core.i18n import (
    Translator,
)
from .functions.info import fetch_info

log = logging.getLogger("tuxbot.cogs.Utils")
_ = Translator("Utils", __file__)


class Utils(commands.Cog, name="Utils"):
    def __init__(self, bot: Tux):
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @command_extra(name="info", aliases=["about"])
    async def _info(self, ctx: ContextPlus):
        proc = psutil.Process()
        infos = fetch_info()

        with proc.oneshot():
            mem = proc.memory_full_info()
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
                value="**Romain#5117:** [git](https://git.gnous.eu/Romain)\n"
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
                    "**{}** physical memory\n**{}** virtual memory",
                    ctx,
                    self.bot.config,
                ).format(
                    humanize.naturalsize(mem.rss),
                    humanize.naturalsize(mem.vms),
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
                value=version_info.info,
                inline=False,
            )

            e.add_field(
                name=_("__:link: Links__", ctx, self.bot.config),
                value="[tuxbot.gnous.eu](https://tuxbot.gnous.eu/) "
                "| [gnous.eu](https://gnous.eu/) "
                "| [git](https://git.gnous.eu/gnouseu/tuxbot-bot) "
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
            title=_("Contributors", ctx, self.bot.config), color=0x36393F
        )

        e.add_field(
            name="**Romain#5117** ",
            value="• [github](https://github.com/Rom1-J)\n"
            "• [gitea](https://git.gnous.eu/Romain)\n"
            "• romain@gnous.eu",
            inline=True,
        )
        e.add_field(
            name="**Outout#4039** ",
            value="• [gitea](https://git.gnous.eu/mael)\n"
            "• [@outoutxyz](https://twitter.com/outouxyz)\n"
            "• mael@gnous.eu",
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
            title=_("Invite", ctx, self.bot.config), color=0x36393F
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
            + f"({discord.utils.oauth_url(self.bot.user.id, basic_perms)})",
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
            + f"({discord.utils.oauth_url(self.bot.user.id, admin_perms)})",
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
