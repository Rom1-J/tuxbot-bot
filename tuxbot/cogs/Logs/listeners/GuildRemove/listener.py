"""
tuxbot.cogs.Logs.listeners.GuildRemove.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever a guild is leaved
"""
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class GuildRemove(commands.Cog):
    """Listener whenever a guild is leaved"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.Cog.listener(name="on_guild_remove")
    async def _on_guild_remove(self, guild: discord.Guild):
        self.bot.statsd.gauge(
            "guilds",
            value=len(self.bot.guilds),
        )