"""
tuxbot.cogs.Admin.commands.Restart.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command to restart Tuxbot
"""

from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot


class RestartCommand(commands.Cog):
    """Restart tuxbot"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command("restart", aliases=["reboot"])
    async def _restart(self, ctx: commands.Context[TuxbotABC]) -> None:
        await ctx.send("*restarting...*")
        await self.bot.shutdown()
