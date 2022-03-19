"""
tuxbot.cogs.Utils.converters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Gives discord member or user
"""

from discord.ext import commands
from discord.ext.commands import Context


class MemberOrUserConverter(commands.Converter):
    """Gives either discord member or user format."""

    # noinspection PyMissingOrEmptyDocstring
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
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
