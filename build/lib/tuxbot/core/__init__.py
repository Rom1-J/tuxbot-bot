from colorama import init

from .. import __version__, version_info, VersionInfo
from .config import Config

__all__ = ["Config", "__version__", "version_info", "VersionInfo"]

init()
