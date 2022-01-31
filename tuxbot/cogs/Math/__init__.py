"""
tuxbot.cogs.Math
~~~~~~~~~~~~~~~~~

Set of useful commands for maths.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.core.Tuxbot import Tuxbot

from .commands.Graph.command import GraphCommand
from .commands.Wolf.command import WolfCommand

STANDARD_COMMANDS = (WolfCommand, GraphCommand)

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=2, minor=0, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


# noinspection PyMissingOrEmptyDocstring
class Commands:
    def __init__(self, bot: Tuxbot):
        for command in STANDARD_COMMANDS:
            bot.add_cog(command(bot=bot))


class Math(ModuleABC, Commands):  # type: ignore
    """Set of useful commands for maths."""
