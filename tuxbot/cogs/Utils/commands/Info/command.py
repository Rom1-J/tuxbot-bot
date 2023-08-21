"""
tuxbot.cogs.Utils.commands.Info.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Shows information about tuxbot
"""

import os
import pathlib
import platform
import typing

import aiofiles
import discord
import humanize
import psutil
from discord.ext import commands

import tuxbot
from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.core.tuxbot import Tuxbot


class InfoCommand(commands.Cog):
    """Shows tuxbot's information."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

        self.stats: dict[str, typing.Any] = {}
        self.app_path = "tuxbot"

    async def cog_load(self: typing.Self) -> None:
        """Fetch bot stats."""
        self.stats = await self.__fetch_info(self.app_path)
        self.bot.logger.info("[InfoCommand] '__fetch_info' done!")

    # =========================================================================
    # =========================================================================

    @staticmethod
    async def __fetch_info(path: str) -> dict[str, typing.Any]:
        """Fetch set of information about tuxbot."""
        total_lines = 0

        total_python_class = 0
        total_python_functions = 0
        total_python_coroutines = 0
        total_python_comments = 0

        file_amount = 0
        python_file_amount = 0

        for p, _, files in os.walk(path):
            for name in files:
                file_dir = str(pathlib.PurePath(p, name))
                if "env" in file_dir:
                    continue

                file_amount += 1

                if name.endswith(".py"):
                    python_file_amount += 1

                    async with aiofiles.open(
                        file_dir, "r", encoding="utf-8"
                    ) as file:
                        async for line in file:
                            _line = line.strip()

                            if _line.startswith("class"):
                                total_python_class += 1

                            if _line.startswith("def"):
                                total_python_functions += 1

                            if _line.startswith("async def"):
                                total_python_coroutines += 1

                            if "#" in _line:
                                total_python_comments += 1

                            total_lines += 1

        return {
            "total_lines": total_lines,
            "total_python_class": total_python_class,
            "total_python_functions": total_python_functions,
            "total_python_coroutines": total_python_coroutines,
            "total_python_comments": total_python_comments,
            "file_amount": file_amount,
            "python_file_amount": python_file_amount,
        }

    # =========================================================================
    # =========================================================================

    @commands.command(name="info", aliases=["about"])
    async def _info(
        self: typing.Self, ctx: commands.Context[TuxbotABC]
    ) -> None:
        proc = psutil.Process()

        if not self.stats:
            self.stats = await self.__fetch_info(self.app_path)

        with proc.oneshot():
            mem = proc.memory_full_info()
            cpu = proc.cpu_percent() / psutil.cpu_count()

            e = discord.Embed(
                title="Information about TuxBot",
                color=0x89C4F9,
            )

            e.add_field(
                name="__:busts_in_silhouette: Development__",
                value=(
                    "**aspheric_:** [git](https://github.com/Rom1-J)\n"
                    "**outout:** [git](https://git.gnous.eu/mael)\n"
                ),
                inline=True,
            )
            e.add_field(
                name=f"__{self.bot.utils.emotes.PYTHON} Python__",
                value=(
                    f"**python** `{platform.python_version()}`\n"
                    f"**discord.py** `{discord.__version__}`"
                ),
                inline=True,
            )
            e.add_field(
                name="__:gear: Usage__",
                value=(
                    f"**{humanize.naturalsize(mem.rss)}** physical memory\n"
                    f"**{humanize.naturalsize(mem.vms)}** virtual memory\n"
                    f"**{cpu:.2f}**% CPU"
                ),
                inline=True,
            )

            e.add_field(
                name="__Servers count__",
                value=str(len(self.bot.guilds)),
                inline=True,
            )
            e.add_field(
                name="__Channels count__",
                value=str(len(list(self.bot.get_all_channels()))),
                inline=True,
            )
            e.add_field(
                name="__Members count__",
                value=str(len(list(self.bot.get_all_members()))),
                inline=True,
            )

            e.add_field(
                name="__:file_folder: Files__",
                value=f"{self.stats.get('file_amount')} "
                f"*({self.stats.get('python_file_amount')}"
                f" {self.bot.utils.emotes.PYTHON})*",
                inline=True,
            )
            e.add_field(
                name="__¶ Lines__",
                value=(
                    f"{self.stats.get('total_lines')} "
                    f"*({self.stats.get('total_python_class')} classes, "
                    f"{self.stats.get('total_python_functions')} functions, "
                    f"{self.stats.get('total_python_coroutines')} coroutines, "
                    f"{self.stats.get('total_python_comments')} comments)*"
                ),
                inline=True,
            )

            e.add_field(
                name="__Latest changes__",
                value=tuxbot.version_info.info,
                inline=False,
            )

            e.add_field(
                name="__:link: Links__",
                value=(
                    "[tuxbot.gnous.eu](https://tuxbot.gnous.eu/) "
                    "| [gnous.eu](https://gnous.eu/) "
                    "| [git](https://github.com/Rom1-J/tuxbot-bot) "
                    "| [status](https://status.gnous.eu/check/154250) "
                    "| [Invite]"
                    "(https://discordapp.com/oauth2/authorize?client_id="
                    "301062143942590465&scope=bot&permissions=268749888)"
                ),
                inline=False,
            )

            e.set_footer(
                text=(
                    f"version: {tuxbot.__version__} "
                    f"• prefix: {ctx.clean_prefix}"
                )
            )

        await ctx.send(embed=e)
