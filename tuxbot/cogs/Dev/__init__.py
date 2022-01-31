"""
tuxbot.cogs.Dev
~~~~~~~~~~~~~~~~

Set of useful commands for developers.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.core.Tuxbot import Tuxbot

from .commands.exceptions import DevException
from .commands.HTTP.command import HTTPCommand

# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Dev.commands ¯\_(ツ)_/¯
# pylint: disable=wrong-import-order
from discord.ext import commands  # isort: skip

STANDARD_COMMANDS = (HTTPCommand,)

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


class Dev(ModuleABC, Commands):  # type: ignore
    """Set of useful commands for developers."""

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: Exception
    ) -> None:
        """Send errors raised by commands"""

        if isinstance(error, DevException):
            await ctx.send(str(error))
