import os
from collections import namedtuple

build = os.popen("/usr/bin/git rev-parse --short HEAD").read().strip()
info = os.popen('/usr/bin/git log -n 3 -s --format="%s"').read().strip()

VersionInfo = namedtuple(
    "VersionInfo", "major minor micro releaselevel build, info"
)
version_info = VersionInfo(
    major=3, minor=0, micro=0, releaselevel="alpha", build=build, info=info
)

__version__ = "v{}.{}.{}-{}.{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.releaselevel,
    version_info.build,
).replace("\n", "")


class ExitCodes:
    CRITICAL = 1
    SHUTDOWN = 0
    RESTART = 42
