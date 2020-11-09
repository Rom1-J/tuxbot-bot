import logging
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
                name=f"__:busts_in_silhouette: "
                f"{_('Development', ctx, self.bot.config)}__",
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
                value=f"**{humanize.naturalsize(mem.rss)}** "
                f"{_('physical memory', ctx, self.bot.config)}\n"
                f"**{humanize.naturalsize(mem.vms)}** "
                f"{_('virtual memory', ctx, self.bot.config)}\n",
                inline=True,
            )

            e.add_field(
                name=f"__{_('Servers count', ctx, self.bot.config)}__",
                value=str(len(self.bot.guilds)),
                inline=True,
            )
            e.add_field(
                name=f"__{_('Channels count', ctx, self.bot.config)}__",
                value=str(len(list(self.bot.get_all_channels()))),
                inline=True,
            )
            e.add_field(
                name=f"__{_('Members count', ctx, self.bot.config)}__",
                value=str(len(list(self.bot.get_all_members()))),
                inline=True,
            )

            e.add_field(
                name=f"__:file_folder: "
                f"{_('Files', ctx, self.bot.config)}__",
                value=f"{infos.get('file_amount')} "
                f"*({infos.get('python_file_amount')}"
                f" <:python:596577462335307777>)*",
                inline=True,
            )
            e.add_field(
                name=f"__¶ {_('Lines', ctx, self.bot.config)}__",
                value=f"{infos.get('total_lines')} "
                f"*({infos.get('total_python_class')} class,"
                f" {infos.get('total_python_functions')} functions,"
                f" {infos.get('total_python_coroutines')} coroutines,"
                f" {infos.get('total_python_comments')} comments)*",
                inline=True,
            )

            e.add_field(
                name=f"__{_('Latest changes', ctx, self.bot.config)}__",
                value=version_info.info,
                inline=False,
            )

            e.add_field(
                name=f"__:link: {_('Links', ctx, self.bot.config)}__",
                value="[tuxbot.gnous.eu](https://tuxbot.gnous.eu/) "
                "| [gnous.eu](https://gnous.eu/) "
                "| [git](https://git.gnous.eu/gnouseu/tuxbot-bot) "
                "| [status](https://status.gnous.eu/check/154250) "
                f"| [{_('Invite', ctx, self.bot.config)}]"
                f"(https://discordapp.com/oauth2/authorize?client_id="
                f"301062143942590465&scope=bot&permissions=268749888)",
                inline=False,
            )

            e.set_footer(
                text=f"version: {__version__} • prefix: {ctx.prefix}"
            )

        await ctx.send(embed=e)
