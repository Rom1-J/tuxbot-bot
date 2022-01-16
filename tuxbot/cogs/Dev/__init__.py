"""
tuxbot.cogs.Dev
~~~~~~~~~~~~~~~~

Set of useful commands for developers.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC

from .commands.HTTPCommand import HTTPCommand


STANDARD_COMMANDS = (HTTPCommand,)


VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=2, minor=0, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Dev(ModuleABC, *STANDARD_COMMANDS):
    """Set of useful commands for developers."""
