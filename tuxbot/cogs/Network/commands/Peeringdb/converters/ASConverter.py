"""
tuxbot.cogs.Network.converters.ASConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converter to ip or domain.
"""

from discord.ext import commands
from discord.ext.commands import Context


class ASConverter(commands.Converter):
    """Clean user input by removing proto."""

    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        return argument.lower().lstrip("as")
