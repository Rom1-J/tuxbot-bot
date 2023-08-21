"""
tuxbot.cogs.Logs.listeners.Ready.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Listener when Tuxbot is ready
"""
import typing

from discord.ext import commands

from tuxbot.core.tuxbot import Tuxbot


class Ready(commands.Cog):
    """Listener when Tuxbot is ready."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_ready")
    async def _on_ready(self: typing.Self) -> None:
        self.bot.statsd.gauge(
            "guilds",
            value=len(self.bot.guilds),
        )
        self.bot.statsd.gauge(
            "members",
            value=sum(guild.member_count or 0 for guild in self.bot.guilds),
        )
        self.bot.statsd.gauge(
            "unique_members",
            value=len(self.bot.users),
        )
