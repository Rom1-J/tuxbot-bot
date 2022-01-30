"""
tuxbot.cogs.Utils
~~~~~~~~~~~~~~~~~~

Set of useful commands for tuxbot.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC

from tuxbot.core.Tuxbot import Tuxbot


from .commands.Credits.command import CreditsCommand
from .commands.Info.command import InfoCommand
from .commands.Invite.command import InviteCommand
from .commands.Source.command import SourceCommand

STANDARD_COMMANDS = (CreditsCommand, InfoCommand, InviteCommand, SourceCommand)


VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=3, minor=0, micro=0, release_level="alpha")

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


class Utils(ModuleABC, Commands):  # type: ignore
    """Set of useful commands for tuxbot."""
