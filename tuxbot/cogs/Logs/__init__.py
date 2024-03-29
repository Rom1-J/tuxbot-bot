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

from ...core.config import config
from .commands.Stats.command import StatsCommand
from .listeners.AppCommandCompletion.listener import AppCommandCompletion
from .listeners.AppCommandError.listener import AppCommandError
from .listeners.CommandCompletion.listener import CommandCompletion
from .listeners.CommandError.listener import CommandError
from .listeners.GuildJoin.listener import GuildJoin
from .listeners.GuildRemove.listener import GuildRemove
from .listeners.Message.listener import Message
from .listeners.Ready.listener import Ready
from .listeners.SocketRawReceive.listener import SocketRawReceive


STANDARD_COMMANDS = (StatsCommand,)

STANDARD_LISTENERS = (
    AppCommandCompletion,
    CommandCompletion,
    CommandError,
    AppCommandError,
    GuildJoin,
    GuildRemove,
    Message,
    Ready,
    SocketRawReceive,
)

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=2, minor=3, micro=0, release_level="stable")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Commands:
    def __init__(self, bot: Tuxbot) -> None:
        if os.getenv("PYTHON_ENV", "production") != "development" and (
            dsn := config.SENTRY_DSN
        ):
            sentry_sdk.init(
                dsn=dsn,
                traces_sample_rate=1.0,
                environment=os.getenv("CLUSTER_ID"),
                debug=False,
                attach_stacktrace=True,
            )

        for command in STANDARD_COMMANDS:
            bot.collection.add_module("Logs", command(bot=bot))

        for listener in STANDARD_LISTENERS:
            bot.collection.add_module("Logs", listener(bot=bot))


class Logs(ModuleABC, Commands):
    """Set of useful statistics commands & workers."""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        super().__init__(bot=self.bot)

    # =========================================================================
