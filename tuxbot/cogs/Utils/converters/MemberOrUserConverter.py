"""
tuxbot.cogs.Utils.converters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gives discord member or user
"""
import typing

import discord
from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC


ConvertType = typing.Union[discord.Member, discord.User, None]


class MemberOrUserConverter(commands.Converter[ConvertType]):
    """Gives either discord member or user format."""

    async def convert(  # type: ignore[override]
        self, ctx: commands.Context[TuxbotABC], argument: str
    ) -> ConvertType:
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
