"""
tuxbot.cogs.Logs.listeners.SocketRawReceive.listener
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Listener whenever websocket message is sent/received
"""

from discord.ext import commands

from tuxbot.core.Tuxbot import Tuxbot


class SocketRawReceive(commands.Cog):
    """Listener whenever websocket message is sent/received"""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

    @commands.Cog.listener(name="on_socket_event_type")
    async def _on_socket_event_type(self, msg):
        if msg not in self.bot.config["disable_events"]:
            self.bot.statsd.increment(
                "socket_event_type", value=1, tags=[f"event_type:{msg}"]
            )
