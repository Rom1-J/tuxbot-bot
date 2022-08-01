"""
tuxbot.cogs.HA
~~~~~~~~~~~~~~~

Set of instructions for High Availability.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.core.Tuxbot import Tuxbot

from .services.Assigner.main import AssignerService
from .services.HTTPServer.main import HTTPServerService


# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Admin.commands ¯\_(ツ)_/¯
# pylint: disable=wrong-import-order
from discord.ext import commands  # isort: skip

STANDARD_SERVICES = (AssignerService, HTTPServerService)

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=3, minor=0, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Services:
    def __init__(self, bot: Tuxbot):
        for service in STANDARD_SERVICES:
            bot.collection.add_module("HA", service(bot=bot))


class HA(ModuleABC, Services):  # type: ignore
    """Set of instructions for High Availability."""

    def __init__(self, bot: Tuxbot):
        self.bot = bot

        super().__init__(bot=self.bot)

    # =========================================================================

    # pylint: disable=invalid-overridden-method
    async def cog_check(self, ctx: commands.Context):
        """Ensure author is owner"""

        return await self.bot.is_owner(ctx.author)
