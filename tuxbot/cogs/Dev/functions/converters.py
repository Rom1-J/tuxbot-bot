from discord.ext import commands
from discord.ext.commands import Context
from tio.tio import AsyncTio

from tuxbot.cogs.Dev.functions.exceptions import (
    UnknownHttpCode,
    TioUnknownLang,
)

from tuxbot.cogs.Dev.functions.http import http_if_exists


def _(x):
    return x


class HttpCodeConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        if argument.isdigit() and (http := http_if_exists(int(argument))):
            return http()

        raise UnknownHttpCode(_("Unknown HTTP code"))


class TioLangConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        tio = AsyncTio()

        if await tio.language_exists(argument):
            return argument

        raise TioUnknownLang(_("Unknown language"))
