"""
tuxbot.cogs.Logs.commands.CommandStats.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Statistics about commands uses
"""

from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class CommandStats(commands.Cog):
    """Shows all command uses stats"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.command(name="commandstats")
    async def _commandstats(self, ctx: commands.Context):
        ...
