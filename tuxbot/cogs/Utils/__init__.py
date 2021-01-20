from collections import namedtuple

from tuxbot.core.bot import Tux
from .utils import Utils
from .config import UtilsConfig, HAS_MODELS

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=2, minor=0, micro=0, release_level="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


def setup(bot: Tux):
    bot.add_cog(Utils(bot))
