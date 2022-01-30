"""
tuxbot.cogs.Admin
~~~~~~~~~~~~~~~~~~

Set of owner only command.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC

from tuxbot.core.Tuxbot import Tuxbot


from .commands.Restart.command import RestartCommand
from .commands.Update.command import UpdateCommand

# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Admin.commands ¯\_(ツ)_/¯
from discord.ext import commands  # pylint: disable=wrong-import-order


STANDARD_COMMANDS = (RestartCommand, UpdateCommand)


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


class Admin(ModuleABC, Commands):  # type: ignore
    """Set of owner only commands."""

    # pylint: disable=invalid-overridden-method
    async def cog_check(self, ctx: commands.Context):
        """Ensure author is owner"""

        if not await self.bot.is_owner(ctx.author):
            raise commands.NotOwner()

        return True
