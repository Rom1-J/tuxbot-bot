"""
tuxbot.cogs.Logs.commands.SocketStats.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Statistics about sockets IO
"""

from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class SocketStats(commands.Cog):
    """Shows all sockets IO stats"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.command(name="socketstats")
    async def _socketstats(self, ctx: commands.Context):
        ...
