"""
tuxbot.cogs.Dev.commands.HTTP.converters.HttpCodeConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converter to ensure user given data is HTTP code.
"""

from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC

from ..exceptions import UnknownHttpCode
from ..http import HttpCode, http_if_exists


ConvertType = HttpCode


class HttpCodeConverter(commands.Converter[ConvertType]):
    """Ensure passed data is HTTP code."""

    async def convert(  # type: ignore[override]
        self, ctx: commands.Context[TuxbotABC], argument: str
    ) -> ConvertType:
        if argument.isdigit() and (http := http_if_exists(int(argument))):
            return http()

        raise UnknownHttpCode("Unknown HTTP code")
