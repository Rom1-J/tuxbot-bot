"""
tuxbot.cogs.Admin.commands.RestartCommand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command to restart Tuxbot
"""
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class RestartCommand(commands.Cog):
    """Restart tuxbot"""
    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.commagnd("restart", aliases=["reboot"])
    async def _restart(self, ctx):
        await ctx.send("*restarting...*")
        await self.bot.shutdown()
