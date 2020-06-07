from collections import namedtuple

from .images import Images
from ...core.bot import Tux

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel")
version_info = VersionInfo(major=1, minor=0, micro=0, releaselevel="alpha")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.releaselevel,
).replace("\n", "")


def setup(bot: Tux):
    bot.add_cog(Images(bot))
