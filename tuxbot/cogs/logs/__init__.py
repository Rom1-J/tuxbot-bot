import logging
from collections import namedtuple

from discord.ext import commands

from .logs import Logs, GatewayHandler, on_error
from ...core.bot import Tux

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel")
version_info = VersionInfo(major=2, minor=0, micro=0, releaselevel="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.releaselevel,
).replace("\n", "")


def setup(bot: Tux):
    cog = Logs(bot)
    bot.add_cog(cog)

    handler = GatewayHandler(cog)
    logging.getLogger().addHandler(handler)
    commands.AutoShardedBot.on_error = on_error
