"""
tuxbot.cogs.Math.commands.Graph.converters.ExprConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.

Converter to parse user expr as sympy expr.
"""
import asyncio
import typing

from discord.ext import commands
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

from tuxbot.abc.tuxbot_abc import TuxbotABC


abc_dict: dict[str, typing.Any] = {}
functions_dict: dict[str, typing.Any] = {}
core_dict: dict[str, typing.Any] = {}
_ExprConverter_T = tuple[str, typing.Any]

exec("from sympy.abc import *", abc_dict)  # noqa: S102
exec("from sympy.functions import *", functions_dict)  # noqa: S102
exec("from sympy.core import *", core_dict)  # noqa: S102

global_dict = abc_dict | functions_dict | core_dict

del global_dict["__builtins__"]


def _parse_expr(argument: str) -> typing.Any | None:
    try:
        return parse_expr(
            argument,
            transformations=(
                *standard_transformations,
                implicit_multiplication_application,
            ),
            evaluate=False,
            global_dict=global_dict,
        )
    except Exception:  # noqa: BLE001
        return None


class ExprConverter(commands.Converter[_ExprConverter_T]):
    """Ensure passed data proper math expression."""

    async def convert(
        self: typing.Self,
        ctx: commands.Context[TuxbotABC],  # noqa: ARG002
        argument: str,
    ) -> _ExprConverter_T:
        argument = argument.rstrip("`").lstrip("`")

        if "_" in argument:
            return _ExprConverter_T((argument, None))

        parsed_arg = await asyncio.get_running_loop().run_in_executor(
            None, _parse_expr, (argument,)
        )

        if isinstance(parsed_arg, bool):
            return _ExprConverter_T((argument, None))

        return _ExprConverter_T((argument, parsed_arg))
