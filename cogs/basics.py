import logging
import os
import pathlib
import platform
import time

import discord
import humanize
import psutil
from discord.ext import commands

from bot import TuxBot
from .utils.lang import Texts
from .utils.extra import commandExtra
from tcp_latency import measure_latency

log = logging.getLogger(__name__)


class Basics(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot

    @staticmethod
    def _latest_commits():
        cmd = 'git log -n 3 -s --format="[\`%h\`](https://git.gnous.eu/gnouseu/tuxbot-bot/commits/%H) %s (%cr)"'

        return os.popen(cmd).read().strip()

    ###########################################################################

    @commandExtra(name='ping', category='basics',
                  description=Texts('commands').get('basics._ping'))
    async def _ping(self, ctx: commands.Context):
        start = time.perf_counter()
        await ctx.trigger_typing()
        end = time.perf_counter()

        latency = round(self.bot.latency * 1000, 2)
        typing = round((end - start) * 1000, 2)
        discordapp = measure_latency(host='google.com', wait=0)[0]

        e = discord.Embed(title='Ping', color=discord.Color.teal())
        e.add_field(name='Websocket', value=f'{latency}ms')
        e.add_field(name='Typing', value=f'{typing}ms')
        e.add_field(name='discordapp.com', value=f'{discordapp}ms')
        await ctx.send(embed=e)

    ###########################################################################

    @staticmethod
    def fetch_info():
        total = 0
        file_amount = 0
        ENV = "env"

        for path, _, files in os.walk("."):
            for name in files:
                file_dir = str(pathlib.PurePath(path, name))
                if not name.endswith(".py") or ENV in file_dir:
                    continue
                file_amount += 1
                with open(file_dir, "r", encoding="utf-8") as file:
                    for line in file:
                        if not line.strip().startswith("#") \
                                or not line.strip():
                            total += 1

        return total, file_amount

    @commandExtra(name='info', aliases=['about'], category='basics',
                  description=Texts('commands').get('basics._info'))
    async def _info(self, ctx: commands.Context):
        proc = psutil.Process()
        lines, files = self.fetch_info()

        with proc.oneshot():
            mem = proc.memory_full_info()
            e = discord.Embed(
                title=Texts('basics', ctx).get('Information about TuxBot'),
                color=0x89C4F9)

            e.add_field(
                name=f"__{Texts('basics', ctx).get('Latest changes')}__",
                value=self._latest_commits(),
                inline=False)

            e.add_field(
                name=f"__:busts_in_silhouette: "
                     f"{Texts('basics', ctx).get('Development')}__",
                value=f"**Romain#5117:** [git](https://git.gnous.eu/Romain)\n"
                      f"**Outout#4039:** [git](https://git.gnous.eu/mael)\n",
                inline=True
            )
            e.add_field(
                name="__<:python:596577462335307777> Python__",
                value=f"**python** `{platform.python_version()}`\n"
                      f"**discord.py** `{discord.__version__}`",
                inline=True
            )
            e.add_field(
                name="__:gear: Usage__",
                value=f"**{humanize.naturalsize(mem.rss)}** "
                      f"{Texts('basics', ctx).get('physical memory')}\n"
                      f"**{humanize.naturalsize(mem.vms)}** "
                      f"{Texts('basics', ctx).get('virtual memory')}\n",
                inline=True
            )

            e.add_field(
                name=f"__{Texts('basics', ctx).get('Servers count')}__",
                value=str(len(self.bot.guilds)),
                inline=True
            )
            e.add_field(
                name=f"__{Texts('basics', ctx).get('Channels count')}__",
                value=str(len([_ for _ in self.bot.get_all_channels()])),
                inline=True
            )
            e.add_field(
                name=f"__{Texts('basics', ctx).get('Members count')}__",
                value=str(len([_ for _ in self.bot.get_all_members()])),
                inline=True
            )

            e.add_field(
                name=f"__:file_folder: {Texts('basics', ctx).get('Files')}__",
                value=str(files),
                inline=True
            )
            e.add_field(
                name=f"__¶ {Texts('basics', ctx).get('Lines')}__",
                value=str(lines),
                inline=True
            )

            e.add_field(
                name=f"__:link: {Texts('basics', ctx).get('Links')}__",
                value="[tuxbot.gnous.eu](https://tuxbot.gnous.eu/) "
                      "| [gnous.eu](https://gnous.eu/) "
                      "| [git](https://git.gnous.eu/gnouseu/tuxbot-bot) "
                      f"| [{Texts('basics', ctx).get('Invite')}](https://discordapp.com/oauth2/authorize?client_id=301062143942590465&scope=bot&permissions=268749888)",
                inline=False
            )

            e.set_footer(text=f'version: {self.bot.version} '
                              f'• prefix: {ctx.prefix}')

        await ctx.send(embed=e)

    ###########################################################################

    @commandExtra(name='credits', aliases=['contributors', 'authors'],
                  category='basics',
                  description=Texts('commands').get('basics._credits'))
    async def _credits(self, ctx: commands.Context):
        e = discord.Embed(
            title=Texts('basics', ctx).get('Contributors'),
            color=0x36393f
        )

        e.add_field(
            name="**Outout#4039** ",
            value="• https://git.gnous.eu/mael        ⠀\n"
                  "• mael@gnous.eu\n"
                  "• [@outoutxyz](https://twitter.com/outouxyz)",
            inline=True
        )
        e.add_field(
            name="**Romain#5117** ",
            value="• https://git.gnous.eu/Romain\n"
                  "• romain@gnous.eu",
            inline=True
        )

        await ctx.send(embed=e)


def setup(bot: TuxBot):
    bot.add_cog(Basics(bot))
