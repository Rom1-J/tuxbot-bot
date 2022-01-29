"""
tuxbot.cogs.Utils
~~~~~~~~~~~~~~~~~~

Set of useful commands for tuxbot.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC

from .commands.Info.command import InfoCommand


STANDARD_COMMANDS = (InfoCommand,)


VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=3, minor=0, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Utils(ModuleABC, *STANDARD_COMMANDS):  # type: ignore
    """Set of useful commands for tuxbot."""
