"""
tuxbot.cogs.Network.converters.IPConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converter to ip or domain.
"""

from discord.ext import commands
from discord.ext.commands import Context


class IPConverter(commands.Converter):
    """Clean user input by removing proto."""

    # noinspection PyMissingOrEmptyDocstring
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        argument = argument.replace("http://", "").replace("https://", "")
        argument = argument.rstrip("/")

        if argument.startswith("`") and argument.endswith("`"):
            argument = argument.lstrip("`").rstrip("`")

        return argument.lower()
