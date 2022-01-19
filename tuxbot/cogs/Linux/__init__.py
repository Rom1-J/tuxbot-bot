"""
tuxbot.cogs.Linux
~~~~~~~~~~~~~~~~~~

Set of useful commands for GNU/Linux users.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC

from .commands.CNF.command import CNFCommand


STANDARD_COMMANDS = (CNFCommand,)


VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=2, minor=0, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Linux(ModuleABC, *STANDARD_COMMANDS):  # type: ignore
    """Set of useful commands for GNU/Linux users."""
