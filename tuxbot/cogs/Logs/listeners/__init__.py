"""
tuxbot.cogs.Logs.listeners
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of useful statistics workers.
"""

from tuxbot.core.Tuxbot import Tuxbot


from .CommandCompletion.listener import CommandCompletion
from .GuildJoin.listener import GuildJoin
from .GuildRemove.listener import GuildRemove
from .Message.listener import Message
from .Ready.listener import Ready
from .SocketRawReceive.listener import SocketRawReceive


STANDARD_LISTENERS = (
    CommandCompletion,
    GuildJoin,
    GuildRemove,
    Message,
    Ready,
    SocketRawReceive,
)


class Listeners:
    """Set of useful statistics workers."""

    def __init__(self, bot: Tuxbot):
        for listener in STANDARD_LISTENERS:
            bot.add_cog(listener(bot=bot))
