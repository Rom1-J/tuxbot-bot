"""
tuxbot.cogs.Logs.listeners.Ready.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener when Tuxbot is ready
"""
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class Ready(commands.Cog):
    """Listener when Tuxbot is ready"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.Cog.listener(name="on_ready")
    async def _on_ready(self):
        self.bot.statsd.gauge(
            "guilds",
            value=len(self.bot.guilds),
        )
        self.bot.statsd.gauge(
            "members",
            value=sum(guild.member_count for guild in self.bot.guilds),
        )
        self.bot.statsd.gauge(
            "unique_members",
            value=len(self.bot.users),
        )
