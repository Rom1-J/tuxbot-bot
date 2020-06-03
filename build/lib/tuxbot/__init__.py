import subprocess
from collections import namedtuple

build = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']) \
    .decode()

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel build')
version_info = VersionInfo(
    major=3, minor=0, micro=0,
    releaselevel='alpha', build=build
)

__version__ = "v{}.{}.{}" \
    .format(version_info.major, version_info.minor, version_info.micro)