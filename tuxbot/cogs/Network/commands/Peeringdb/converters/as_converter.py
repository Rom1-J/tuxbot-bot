"""
tuxbot.cogs.Network.converters.ASConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Converter to ip or domain.
"""
import typing

from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC


_ASConverter_T = str


class ASConverter(commands.Converter[_ASConverter_T]):
    """Clean user input by removing proto."""

    async def convert(
        self: typing.Self,
        ctx: commands.Context[TuxbotABC],  # noqa: ARG002
        argument: str,
    ) -> _ASConverter_T:
        return argument.lower().lstrip("as")
