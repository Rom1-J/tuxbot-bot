"""
tuxbot.cogs.Dev.commands.HTTP.converters.HttpCodeConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Converter to ensure user given data is HTTP code.
"""
import typing

from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC
from tuxbot.cogs.Dev.commands.HTTP.exceptions import UnknownHttpCode
from tuxbot.cogs.Dev.commands.HTTP.http import HttpCode, http_if_exists


_HttpCodeConverter_T = HttpCode


class HttpCodeConverter(commands.Converter[_HttpCodeConverter_T]):
    """Ensure passed data is HTTP code."""

    async def convert(
        self: typing.Self,
        ctx: commands.Context[TuxbotABC],  # noqa: ARG002
        argument: str,
    ) -> _HttpCodeConverter_T:
        if argument.isdigit():
            http = http_if_exists(int(argument))

            if http is not None:
                return http

        msg = "Unknown HTTP code"
        raise UnknownHttpCode(msg)
