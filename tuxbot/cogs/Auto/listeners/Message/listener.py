"""
tuxbot.cogs.Logs.listeners.Message.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever message is sent
"""
import discord
from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot

from .workers import Worker


class Message(commands.Cog):
    """Listener whenever message is sent"""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot
        self.worker = Worker(self.bot)

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_message")
    async def _on_message(self, message: discord.Message) -> None:
        await self.worker.runs(message)
