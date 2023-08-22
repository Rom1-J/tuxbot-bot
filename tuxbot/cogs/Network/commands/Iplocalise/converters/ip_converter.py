"""
tuxbot.cogs.Network.converters.IPConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Converter to ip or domain.
"""
import typing
from urllib.parse import urlparse

from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC


_IPConverter_T = str


class IPConverter(commands.Converter[_IPConverter_T]):
    """Clean user input by removing proto."""

    async def convert(
        self: typing.Self,
        ctx: commands.Context[TuxbotABC],  # noqa: ARG002
        argument: str,
    ) -> _IPConverter_T:
        argument = argument.lstrip("`").rstrip("`")

        return urlparse(argument).netloc
