"""
tuxbot.cogs.Math.commands
~~~~~~~~~~~~~~~~~~~~~~~~~~

Set of useful commands for maths.
"""

from tuxbot.core.Tuxbot import Tuxbot

from .Graph.command import GraphCommand
from .Wolf.command import WolfCommand

STANDARD_COMMANDS = (WolfCommand, GraphCommand)


class Commands:
    """Set of useful commands for maths."""

    def __init__(self, bot: Tuxbot):
        for command in STANDARD_COMMANDS:
            bot.add_cog(command(bot=bot))
