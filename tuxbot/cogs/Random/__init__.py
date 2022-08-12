"""
tuxbot.cogs.Random
~~~~~~~~~~~~~~~~~~~

Set of random commands for tuxbot.
"""
from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from .commands.Cat.command import CatCommand
from .commands.Coin.command import CoinCommand
from .commands.Dog.command import DogCommand
from .commands.Duck.command import DuckCommand
from .commands.exceptions import RandomException
from .commands.Koala.command import KoalaCommand
from .commands.RedPanda.command import RedPandaCommand


# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Utils.commands ¯\_(ツ)_/¯
# pylint: disable=wrong-import-order
from discord.ext import commands  # isort: skip

STANDARD_COMMANDS = (
    CatCommand,
    CoinCommand,
    DogCommand,
    DuckCommand,
    KoalaCommand,
    RedPandaCommand,
)

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=1, minor=3, micro=0, release_level="stable")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Commands:
    def __init__(self, bot: Tuxbot) -> None:
        for command in STANDARD_COMMANDS:
            bot.collection.add_module("Random", command(bot=bot))


class Random(ModuleABC, Commands):
    """Set of random commands for tuxbot."""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        super().__init__(bot=self.bot)

    # =========================================================================

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context[TuxbotABC], error: Exception
    ) -> None:
        """Send errors raised by commands"""

        if isinstance(error, RandomException):
            await ctx.send(str(error))
