"""
tuxbot.cogs.Auto
~~~~~~~~~~~~~~~~~

Set of useful automatic workers.
"""
from collections import namedtuple

import discord

from tuxbot.abc.ModuleABC import ModuleABC
from tuxbot.abc.TuxbotABC import TuxbotABC
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
version_info = VersionInfo(major=1, minor=1, micro=0, release_level="stable")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Commands:
    def __init__(self, bot: Tuxbot) -> None:
        for command in STANDARD_COMMANDS:
            bot.collection.add_module("Auto", command(bot=bot))

        for listener in STANDARD_LISTENERS:
            bot.collection.add_module("Auto", listener(bot=bot))


class Auto(ModuleABC, Commands):
    """Set of useful automatic workers."""

    def __init__(self, bot: Tuxbot) -> None:
        self.bot = bot

        super().__init__(bot=self.bot)

    # =========================================================================

    async def cog_check(  # type: ignore[override]
        self, ctx: commands.Context[TuxbotABC]
    ) -> bool:
        if ctx.guild and isinstance(ctx.author, discord.Member):
            return bool(ctx.author.guild_permissions.administrator)

        return False
