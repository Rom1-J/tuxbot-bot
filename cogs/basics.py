import platform
import time

import discord
import humanize
import psutil
from discord.ext import commands

from bot import TuxBot
from .utils.lang import Texts


class Basics(commands.Cog):

    def __init__(self, bot: TuxBot):
        self.bot = bot

    """---------------------------------------------------------------------"""

    @commands.command(name='ping')
    async def _ping(self, ctx: commands.Context):
        start = time.perf_counter()
        await ctx.trigger_typing()
        end = time.perf_counter()

        latency = round(self.bot.latency * 1000, 2)
        typing = round((end - start) * 1000, 2)

        e = discord.Embed(title='Ping', color=discord.Color.teal())
        e.add_field(name='Websocket', value=f'{latency}ms')
        e.add_field(name='Typing', value=f'{typing}ms')
        await ctx.send(embed=e)

    """---------------------------------------------------------------------"""

    @commands.command(name='info')
    async def _info(self, ctx: commands.Context):
        proc = psutil.Process()
        with proc.oneshot():
            mem = proc.memory_full_info()
            e = discord.Embed(
                title=f"{Texts('basics').get('Information about TuxBot')}",
                color=0x89C4F9)
            e.add_field(
                name=f"__:busts_in_silhouette: "
                     f"{Texts('basics').get('Development')}__",
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
                      f"{Texts('basics').get('physical memory')}\n"
                      f"**{humanize.naturalsize(mem.vms)}** "
                      f"{Texts('basics').get('virtual memory')}\n",
                inline=True
            )

            e.add_field(
                name=f"__{Texts('basics').get('Servers count')}__",
                value=str(len(self.bot.guilds)),
                inline=True
            )
            e.add_field(
                name=f"__{Texts('basics').get('Channels count')}__",
                value=str(len([_ for _ in self.bot.get_all_channels()])),
                inline=True
            )
            e.add_field(
                name=f"__{Texts('basics').get('Members count')}__",
                value=str(len([_ for _ in self.bot.get_all_members()])),
                inline=True
            )

            e.set_footer(text=f'version: {self.bot.version}')

        await ctx.send(embed=e)


def setup(bot: TuxBot):
    bot.add_cog(Basics(bot))
