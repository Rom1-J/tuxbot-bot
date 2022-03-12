"""
tuxbot.cogs.Utils
~~~~~~~~~~~~~~~~~~

Set of useful commands for tuxbot.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.core.Tuxbot import Tuxbot

from .commands.Credits.command import CreditsCommand
from .commands.exceptions import UtilsException
from .commands.Info.command import InfoCommand
from .commands.Invite.command import InviteCommand
from .commands.Ping.command import PingCommand
from .commands.Quote.command import QuoteCommand
from .commands.Source.command import SourceCommand
from .commands.UI.command import UICommand

# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Utils.commands ¯\_(ツ)_/¯
# pylint: disable=wrong-import-order
from discord.ext import commands  # isort: skip

STANDARD_COMMANDS = (
    CreditsCommand,
    InfoCommand,
    InviteCommand,
    PingCommand,
    QuoteCommand,
    SourceCommand,
    UICommand,
)

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

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: Exception
    ) -> None:
        """Send errors raised by commands"""

        if isinstance(error, UtilsException):
            await ctx.send(str(error))
