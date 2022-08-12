"""
tuxbot.cogs.Network.converters.IPConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converter to ip or domain.
"""

from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC


ConvertType = str


class IPConverter(commands.Converter[ConvertType]):
    """Clean user input by removing proto."""

    async def convert(  # type: ignore
        self, ctx: commands.Context[TuxbotABC], argument: str
    ) -> ConvertType:
        argument = argument.replace("http://", "").replace("https://", "")
        argument = argument.split("/")[0]

        argument = argument.lstrip("`").rstrip("`")

        return argument.lower()
