"""
tuxbot.cogs.Auto
~~~~~~~~~~~~~~~~~.

Set of useful automatic workers.
"""
import typing

import discord

from tuxbot.abc.module_abc import ModuleABC
from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.core.tuxbot import Tuxbot

from .commands.AutoPin.command import AutoPinCommand
from .commands.AutoQuote.command import AutoQuoteCommand
from .listeners.Message.listener import Message
from .listeners.RawReactionAdd.listener import RawReactionAdd


# Note: for some reasons, this import must be done after tuxbot.* imports.
# If it isn't, commands is bind on tuxbot.cogs.Admin.commands ¯\_(ツ)_/¯
# pylint: disable=wrong-import-order
from discord.ext import commands  # isort: skip


STANDARD_COMMANDS = (AutoPinCommand, AutoQuoteCommand)

STANDARD_LISTENERS = (Message, RawReactionAdd)


class VersionInfo(typing.NamedTuple):
    major: int
    minor: int
    micro: int
    release_level: str


version_info = VersionInfo(major=1, minor=2, micro=0, release_level="stable")

__version__ = "v{}.{}.{}-{}".format(
    version_info.major,
    version_info.minor,
    version_info.micro,
    version_info.release_level,
).replace("\n", "")


class Commands:
    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        for command in STANDARD_COMMANDS:
            bot.collection.add_module("Auto", command(bot=bot))

        for listener in STANDARD_LISTENERS:
            bot.collection.add_module("Auto", listener(bot=bot))


class Auto(ModuleABC, Commands):
    """Set of useful automatic workers."""

    def __init__(self: typing.Self, bot: Tuxbot) -> None:
        self.bot = bot

        super().__init__(bot=self.bot)

    # =========================================================================

    async def cog_check(
        self: typing.Self, ctx: commands.Context[TuxbotABC]
    ) -> bool:
        if ctx.guild and isinstance(ctx.author, discord.Member):
            return bool(ctx.author.guild_permissions.administrator)

        return False
