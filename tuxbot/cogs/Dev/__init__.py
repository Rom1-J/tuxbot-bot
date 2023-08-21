"""
tuxbot.cogs.Dev
~~~~~~~~~~~~~~~~.

Set of useful commands for developers.
"""
import typing

from tuxbot.abc.module_abc import ModuleABC
from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.core.tuxbot import Tuxbot

from .commands.exceptions import DevException
from .commands.HTTP.command import HTTPCommand


# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Dev.commands ¯\_(ツ)_/¯
# pylint: disable=wrong-import-order
from discord.ext import commands  # isort: skip

STANDARD_COMMANDS = (HTTPCommand,)


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


class Commands:
    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        for command in STANDARD_COMMANDS:
            bot.collection.add_module("Dev", command(bot=bot))


class Dev(ModuleABC, Commands):
    """Set of useful commands for developers."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

        super().__init__(bot=self.bot)

    # =========================================================================

    @commands.Cog.listener()
    async def on_command_error(
        self: typing.Self, ctx: commands.Context[TuxbotABC], error: Exception
    ) -> None:
        """Send errors raised by commands."""
        if isinstance(error, DevException):
            await ctx.send(str(error))
