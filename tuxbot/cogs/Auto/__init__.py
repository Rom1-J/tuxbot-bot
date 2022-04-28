"""
tuxbot.cogs.Auto
~~~~~~~~~~~~~~~~~

Set of useful automatic workers.
"""
from collections import namedtuple

import discord

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.core.Tuxbot import Tuxbot

from .commands.AutoQuote.command import AutoQuoteCommand
from .listeners.Message.listener import Message


# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Admin.commands ¯\_(ツ)_/¯
# pylint: disable=wrong-import-order
from discord.ext import commands  # isort: skip


STANDARD_COMMANDS = (AutoQuoteCommand,)

STANDARD_LISTENERS = (Message,)

VersionInfo = namedtuple("VersionInfo", "major minor micro release_level")
version_info = VersionInfo(major=1, minor=0, micro=0, release_level="beta")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


# noinspection PyMissingOrEmptyDocstring
class Commands:
    def __init__(self, bot: Tuxbot):
        # noinspection PyTypeChecker
        for command in STANDARD_COMMANDS:
            bot.collection.add_module("Auto", command(bot=bot))

        for listener in STANDARD_LISTENERS:
            bot.collection.add_module("Auto", listener(bot=bot))


class Auto(ModuleABC, Commands):  # type: ignore
    """Set of useful automatic workers."""

    # pylint: disable=invalid-overridden-method
    async def cog_check(self, ctx: commands.Context):
        """Ensure author is owner"""

        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(
                [discord.Permissions.administrator]
            )

        return True
