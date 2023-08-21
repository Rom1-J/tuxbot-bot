"""
tuxbot.cogs.Network.converters.ASConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Converter to ip or domain.
"""
import typing

from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC


ConvertType = str


class ASConverter(commands.Converter[ConvertType]):
    """Clean user input by removing proto."""

    async def convert(
        self: typing.Self,
        ctx: commands.Context[TuxbotABC],  # noqa: ARG002
        argument: str,
    ) -> ConvertType:
        return argument.lower().lstrip("as")
