from collections import namedtuple

from tuxbot.core.bot import Tux
from .dev import Dev
from .config import DevConfig, HAS_MODELS

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=0, minor=1, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


def setup(bot: Tux):
    cog = Dev(bot)
    bot.add_cog(cog)
