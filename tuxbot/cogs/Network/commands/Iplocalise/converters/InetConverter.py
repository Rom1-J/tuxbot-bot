"""
tuxbot.cogs.Network.converters.InetConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converter to inet.
"""
import typing

from discord.ext import commands

from tuxbot.abc.TuxbotABC import TuxbotABC


ConvertType = typing.Optional[int]


class InetConverter(commands.Converter[ConvertType]):
    """Clean and return inet."""

    async def convert(  # type: ignore[override]
        self, ctx: commands.Context[TuxbotABC], argument: str | None
    ) -> ConvertType:
        res = None

        if not argument:
            return res

        if "6" in argument:
            res = 6

        if "4" in argument:
            res = 4

        return res
