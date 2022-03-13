"""
tuxbot.cogs.Logs
~~~~~~~~~~~~~~~~~

Set of useful statistics commands & workers.
"""
import os
from collections import namedtuple

import sentry_sdk

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.core.Tuxbot import Tuxbot

from .commands.Stats.command import StatsCommand
from .listeners.CommandCompletion.listener import CommandCompletion
from .listeners.CommandError.listener import CommandError
from .listeners.GuildJoin.listener import GuildJoin
from .listeners.GuildRemove.listener import GuildRemove
from .listeners.Message.listener import Message
from .listeners.Ready.listener import Ready
from .listeners.SocketRawReceive.listener import SocketRawReceive

STANDARD_COMMANDS = (StatsCommand,)

STANDARD_LISTENERS = (
    CommandCompletion,
    CommandError,
    GuildJoin,
    GuildRemove,
    Message,
    Ready,
    SocketRawReceive,
)

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=2, minor=1, micro=0, release_level="stable")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


# noinspection PyMissingOrEmptyDocstring
class Commands:
    def __init__(self, bot: Tuxbot):
        if os.getenv("PYTHON_ENV", "production") != "development":
            # pylint: disable=abstract-class-instantiated
            sentry_sdk.init(
                dsn=bot.config["sentry"].get("dsn"),
                traces_sample_rate=1.0,
                environment=os.getenv("CLUSTER_ID"),
                debug=False,
                attach_stacktrace=True,
            )

        # noinspection PyTypeChecker
        for command in STANDARD_COMMANDS + STANDARD_LISTENERS:
            bot.add_cog(command(bot=bot))


class Logs(ModuleABC, Commands):  # type: ignore
    """Set of useful statistics commands & workers."""
