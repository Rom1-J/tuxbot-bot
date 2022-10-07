"""
tuxbot.cogs.Tags
~~~~~~~~~~~~~~~~~

Set of useful commands for tags.
"""
from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.abc.TuxbotABC import TuxbotABC
from tuxbot.core.Tuxbot import Tuxbot

from .commands.exceptions import TagsException
from .commands.Tag.command import TagCommand


# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Utils.commands ¯\_(ツ)_/¯
# pylint: disable=wrong-import-order
from discord.ext import commands  # isort: skip

STANDARD_COMMANDS = (TagCommand,)

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=2, minor=1, micro=1, release_level="stable")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Commands:
    def __init__(self, bot: Tuxbot) -> None:
        for command in STANDARD_COMMANDS:
            bot.collection.add_module("Tags", command(bot=bot))


class Tags(ModuleABC, Commands):
    """Set of useful commands for tags."""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        super().__init__(bot=self.bot)

    # =========================================================================

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context[TuxbotABC], error: Exception
    ) -> None:
        """Send errors raised by commands"""

        if isinstance(error, TagsException):
            await ctx.send(str(error))

    # =========================================================================
    # =========================================================================

    @commands.command(name="tag")
    async def _tag_deprecated(self, ctx: commands.Context[TuxbotABC]) -> None:
        await ctx.send(
            "Deprecated command, use /tag instead "
            "(reinvite the bot if application commands are not enabled)",
            delete_after=5,
        )
