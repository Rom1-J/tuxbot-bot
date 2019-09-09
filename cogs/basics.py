import platform
import socket

import discord
from discord.ext import commands
from discord.http import Route


class Basics(commands.Cog):
    """Commandes générales."""

    def __init__(self, bot: discord.ext.commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: discord.ext.commands.context.Context):
        delta = await ctx.send(self.bot.latency * 1000)
        await ctx.send((delta.created_at-ctx.message.created_at)
                       .microseconds/1000)

    """---------------------------------------------------------------------"""

    @commands.command()
    async def info(self, ctx):
        """Affiches des informations sur le bot"""
        text = open('texts/info.md').read()
        os_info = str(platform.system()) + " / " + str(platform.release())
        em = discord.Embed(title='Informations sur TuxBot',
                           description=text.format(os_info,
                                                   platform.python_version(),
                                                   socket.gethostname(),
                                                   discord.__version__,
                                                   Route.BASE),
                           colour=0x89C4F9)
        em.set_footer(text="/home/****/bot.py")
        await ctx.send(embed=em)

    """---------------------------------------------------------------------"""

    @commands.command()
    async def help(self, ctx):
        """Affiches l'aide du bot"""
        text = open('texts/help.md').read().split("[split]")
        for txt in text:
            em = discord.Embed(title='Commandes de TuxBot', description=txt,
                               colour=0x89C4F9)
            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Basics(bot))
