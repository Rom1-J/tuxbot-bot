"""
tuxbot.cogs.Polls
~~~~~~~~~~~~~~~~~

Set of useful commands for polls.
"""
from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from .commands.exceptions import PollsException
from .commands.Poll.command import PollCommand
from .listeners.RawReactionAdd.listener import RawReactionAdd
from .listeners.RawReactionRemove.listener import RawReactionRemove


# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Utils.commands ¯\_(ツ)_/¯
# pylint: disable=wrong-import-order
from discord.ext import commands  # isort: skip


STANDARD_COMMANDS = (PollCommand,)

STANDARD_LISTENERS = (
    RawReactionAdd,
    RawReactionRemove,
)

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=3, minor=0, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Commands:
    def __init__(self, bot: Tuxbot) -> None:
        for command in STANDARD_COMMANDS:
            bot.collection.add_module("Polls", command(bot=bot))

        for listener in STANDARD_LISTENERS:
            bot.collection.add_module("Polls", listener(bot=bot))


class Polls(ModuleABC, Commands):
    """Set of useful commands for polls."""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        super().__init__(bot=self.bot)

    # =========================================================================

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context[TuxbotABC], error: Exception
    ) -> None:
        """Send errors raised by commands"""

        if isinstance(error, PollsException):
            await ctx.send(str(error))

    # =========================================================================
    # =========================================================================

    @commands.command(name="poll")
    async def _poll_deprecated(self, ctx: commands.Context[TuxbotABC]) -> None:
        await ctx.send(
            "Deprecated command, use /poll instead "
            "(reinvite the bot if application commands are not enabled)",
            delete_after=5,
        )
