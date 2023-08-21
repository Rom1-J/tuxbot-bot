"""
tuxbot.cogs.Network.converters.InetConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Converter to inet.
"""
import typing

from discord.ext import commands

from tuxbot.abc.tuxbot_abc import TuxbotABC


ConvertType = int | None


class InetConverter(commands.Converter[ConvertType]):
    """Clean and return inet."""

    async def convert(
        self: typing.Self,
        ctx: commands.Context[TuxbotABC],  # noqa: ARG002
        argument: str | None,
    ) -> ConvertType:
        res = None

        if not argument:
            return res

        if "6" in argument:
            res = 6

        if "4" in argument:
            res = 4

        return res
