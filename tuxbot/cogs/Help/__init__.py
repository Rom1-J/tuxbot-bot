"""
tuxbot.cogs.Help
~~~~~~~~~~~~~~~~~

Tuxbot help command.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.core.Tuxbot import Tuxbot

from .commands.Help.command import HelpCommand


VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=2, minor=1, micro=0, release_level="stable")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Help(ModuleABC):
    """Tuxbot help command."""

    def __init__(self, bot: Tuxbot) -> None:
        self.old_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    # =========================================================================

    async def cog_unload(self) -> None:
        """Rebind native dpy help command before unload"""
        self.bot.help_command = self.old_help_command
