"""
tuxbot.cogs.Dev.converters.HttpCodeConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converter to ensure user given data is HTTP code.
"""

from discord.ext import commands
from discord.ext.commands import Context

from ..functions.exceptions import UnknownHttpCode
from ..functions.http import http_if_exists


def _(x):
    return x


class HttpCodeConverter(commands.Converter):
    """Ensure passed data is HTTP code."""

    # noinspection PyMissingOrEmptyDocstring
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if argument.isdigit() and (http := http_if_exists(int(argument))):
            return http()

        raise UnknownHttpCode(_("Unknown HTTP code"))
