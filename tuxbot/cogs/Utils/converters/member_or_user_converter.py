"""
tuxbot.cogs.Utils.converters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Gives discord member or user
"""
import typing

import discord
from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC


_MemberOrUserConverter_T = discord.Member | discord.User | None


class MemberOrUserConverter(commands.Converter[_MemberOrUserConverter_T]):
    """Gives either discord member or user format."""

    async def convert(
        self: typing.Self, ctx: commands.Context[TuxbotABC], argument: str
    ) -> _MemberOrUserConverter_T:
        if argument:
            try:
                return await commands.MemberConverter().convert(ctx, argument)
            except commands.MemberNotFound:
                pass

            try:
                return await commands.UserConverter().convert(ctx, argument)
            except commands.UserNotFound:
                pass

        return None
