"""
tuxbot.cogs.Admin
~~~~~~~~~~~~~~~~~~

Set of owner only command.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.core.Tuxbot import Tuxbot

from ...abc.TuxbotABC import TuxbotABC
from .commands.Restart.command import RestartCommand
from .commands.Sync.command import SyncCommand
from .commands.Update.command import UpdateCommand


# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Admin.commands ¯\_(ツ)_/¯
# pylint: disable=wrong-import-order
from discord.ext import commands  # isort: skip


STANDARD_COMMANDS = (RestartCommand, SyncCommand, UpdateCommand)

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=3, minor=1, micro=0, release_level="stable")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Commands:
    def __init__(self, bot: Tuxbot) -> None:
        for command in STANDARD_COMMANDS:
            bot.collection.add_module("Admin", command(bot=bot))


class Admin(ModuleABC, Commands):
    """Set of owner only commands."""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        super().__init__(bot=self.bot)

    # =========================================================================

    async def cog_check(  # type: ignore[override]
        self, ctx: commands.Context[TuxbotABC]
    ) -> bool:
        return bool(await self.bot.is_owner(ctx.author))  # type: ignore
