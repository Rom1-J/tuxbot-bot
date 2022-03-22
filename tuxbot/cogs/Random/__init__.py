"""
tuxbot.cogs.Random
~~~~~~~~~~~~~~~~~~~

Set of random commands for tuxbot.
"""
from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.core.Tuxbot import Tuxbot

from .commands.Coin.command import CoinCommand
from .commands.Duck.command import DuckCommand
from .commands.exceptions import RandomException


# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Utils.commands ¯\_(ツ)_/¯
# pylint: disable=wrong-import-order
from discord.ext import commands  # isort: skip

STANDARD_COMMANDS = (
    CoinCommand,
    DuckCommand,
)

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=1, minor=0, micro=0, release_level="stable")

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
            bot.collection.add_module("Random", command(bot=bot))


class Random(ModuleABC, Commands):  # type: ignore
    """Set of random commands for tuxbot."""

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: Exception
    ) -> None:
        """Send errors raised by commands"""

        if isinstance(error, RandomException):
            await ctx.send(str(error))
