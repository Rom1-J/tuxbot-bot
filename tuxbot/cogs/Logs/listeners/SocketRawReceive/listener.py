"""
tuxbot.cogs.Logs.listeners.SocketRawReceive.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Listener whenever websocket message is sent/received
"""
import typing

from discord.ext import commands

from tuxbot.core.config import config
from tuxbot.core.tuxbot import Tuxbot


class SocketRawReceive(commands.Cog):
    """Listener whenever websocket message is sent/received."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

    # =========================================================================
    # =========================================================================

    @commands.Cog.listener(name="on_socket_event_type")
    async def _on_socket_event_type(self: typing.Self, msg: str) -> None:
        if msg not in config.CLIENT["disabled_events"]:
            self.bot.statsd.incr(f"event.{msg}", 1)
