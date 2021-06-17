from collections import namedtuple

from tuxbot.core.bot import Tux
from .math import Math
from .config import MathConfig, HAS_MODELS

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=1, minor=0, micro=2, release_level="stable")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


def setup(bot: Tux):
    bot.add_cog(Math(bot, version_info))
