"""
tuxbot.cogs.Admin.commands.Restart.command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Command to restart Tuxbot
"""
import typing

from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.core.tuxbot import Tuxbot


class RestartCommand(commands.Cog):
    """Restart tuxbot."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.command("restart", aliases=["reboot"])
    async def _restart(
        self: typing.Self, ctx: commands.Context[TuxbotABC]
    ) -> None:
        await ctx.send("*restarting...*")
        await self.bot.shutdown()
