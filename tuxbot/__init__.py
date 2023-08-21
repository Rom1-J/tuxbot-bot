"""
Tuxbot
~~~~~~~.

bot made initially for https://gnous.eu, then proposed to the entire
free software community
"""
import os
import typing


build = (
    os.popen("/usr/bin/git rev-parse --short HEAD")  # noqa: S605
    .read()
    .strip()
)
info = (
    os.popen("/usr/bin/git log -n 3 -s --format='%s'")  # noqa: S605
    .read()
    .strip()
)


class VersionInfo(typing.NamedTuple):
    major: int
    minor: int
    micro: int
    release_level: str
    build: str
    info: str


version_info = VersionInfo(
    major=4, minor=3, micro=0, release_level="beta", build=build, info=info
)

__version__ = "v{}.{}.{}-{}+{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
    version_info.build,
).replace("\n", "")
