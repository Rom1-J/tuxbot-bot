import logging
from collections import namedtuple

from discord.ext import commands

from tuxbot.core.bot import Tux
from .logs import Logs, GatewayHandler
from .config import LogsConfig, HAS_MODELS

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=1, minor=0, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


def setup(bot: Tux):
    cog = Logs(bot)
    bot.add_cog(cog)

    handler = GatewayHandler(cog)
    logging.getLogger().addHandler(handler)
