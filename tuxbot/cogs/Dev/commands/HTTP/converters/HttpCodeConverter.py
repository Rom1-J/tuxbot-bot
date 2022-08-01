"""
tuxbot.cogs.Dev.commands.HTTP.converters.HttpCodeConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converter to ensure user given data is HTTP code.
"""

from discord.ext import commands
from discord.ext.commands import Context

from ..exceptions import UnknownHttpCode
from ..http import http_if_exists


class HttpCodeConverter(commands.Converter):
    """Ensure passed data is HTTP code."""

    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if argument.isdigit() and (http := http_if_exists(int(argument))):
            return http()  # type: ignore

        raise UnknownHttpCode("Unknown HTTP code")
