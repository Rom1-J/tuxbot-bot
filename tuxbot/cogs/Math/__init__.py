"""
tuxbot.cogs.Math
~~~~~~~~~~~~~~~~~

Set of useful commands for maths.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC

from .commands.Wolf.command import WolfCommand
from .commands.Graph.command import GraphCommand


STANDARD_COMMANDS = (WolfCommand, GraphCommand)


VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=2, minor=0, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Math(ModuleABC, *STANDARD_COMMANDS):  # type: ignore
    """Set of useful commands for maths."""
