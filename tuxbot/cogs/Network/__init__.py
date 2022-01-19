"""
tuxbot.cogs.Network
~~~~~~~~~~~~~~~~~~~~

Set of useful commands for networking.
"""

from collections import namedtuple

from tuxbot.abc.ModuleABC import ModuleABC

from .commands.Iplocalise.command import IplocaliseCommand
from .commands.Peeringdb.command import PeeringdbCommand
from .commands.Dig.command import DigCommand

# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Admin.commands ¯\_(ツ)_/¯
from discord.ext import commands  # pylint: disable=wrong-import-order

from ...core.Tuxbot import Tuxbot

STANDARD_COMMANDS = (IplocaliseCommand, PeeringdbCommand, DigCommand)


VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=3, minor=0, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Network(ModuleABC, *STANDARD_COMMANDS):  # type: ignore
    """Set of useful commands for networking."""

    async def cog_before_invoke(self, ctx: commands.Context):
        await ctx.trigger_typing()
