"""
tuxbot.cogs.Logs.listeners.Message.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever message is sent
"""
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class Message(commands.Cog):
    """Listener whenever message is sent"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_message")
    async def _on_message(self, message: discord.Message) -> None:
        if message.guild:
            tags = [f"guild:{message.guild.id}"]
        else:
            tags = [f"private:{message.channel.id}"]

        self.bot.statsd.increment("messages", value=1, tags=tags)
