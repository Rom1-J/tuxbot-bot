"""
tuxbot.cogs.Help
~~~~~~~~~~~~~~~~~.

Tuxbot help command.
"""
import typing

from tuxbot.abc.module_abc import ModuleABC
from tuxbot.core.tuxbot import Tuxbot

from .commands.Help.command import HelpCommand


class VersionInfo(typing.NamedTuple):
    major: int
    minor: int
    micro: int
    release_level: str


version_info = VersionInfo(major=2, minor=1, micro=0, release_level="stable")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Help(ModuleABC):
    """Tuxbot help command."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.old_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    # =========================================================================

    async def cog_unload(self: typing.Self) -> None:
        """Rebind native dpy help command before unload."""
        self.bot.help_command = self.old_help_command
