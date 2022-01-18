"""
tuxbot.cogs.Network.converters.InetConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converter to inet.
"""

from discord.ext import commands
from discord.ext.commands import Context


class InetConverter(commands.Converter):
    """Clean and return inet."""

    # noinspection PyMissingOrEmptyDocstring
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if "6" in argument:
            return 6

        if "4" in argument:
            return 4

        return None
