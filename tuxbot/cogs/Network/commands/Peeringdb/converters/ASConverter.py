"""
tuxbot.cogs.Network.converters.ASConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converter to ip or domain.
"""

from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC


ConvertType = str


class ASConverter(commands.Converter[ConvertType]):
    """Clean user input by removing proto."""

    async def convert(  # type: ignore
        self, ctx: commands.Context[TuxbotABC], argument: str
    ) -> ConvertType:
        return argument.lower().lstrip("as")
