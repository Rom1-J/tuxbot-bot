"""
tuxbot.cogs.Math.commands.Graph.converters.ExprConverter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

from tuxbot.abc.TuxbotABC import TuxbotABC


abc_dict: dict[str, typing.Any] = {}
functions_dict: dict[str, typing.Any] = {}
core_dict: dict[str, typing.Any] = {}
ConvertType = tuple[str, typing.Any]

# pylint: disable=exec-used
exec("from sympy.abc import *", abc_dict)
exec("from sympy.functions import *", functions_dict)
exec("from sympy.core import *", core_dict)

global_dict = abc_dict | functions_dict | core_dict

del global_dict["__builtins__"]


class ExprConverter(commands.Converter[ConvertType]):
    """Ensure passed data is HTTP code."""

    async def convert(  # type: ignore[override]
        self, ctx: commands.Context[TuxbotABC], argument: str
    ) -> ConvertType:
        argument = argument.rstrip("`").lstrip("`")

        if "_" in argument:
            return argument, None

        def _parse_expr() -> typing.Any | None:
            try:
                return parse_expr(  # type: ignore[no-untyped-call]
                    argument,
                    transformations=(
                        standard_transformations
                        + (implicit_multiplication_application,)
                    ),
                    evaluate=False,
                    global_dict=global_dict,
                )
            except Exception:
                return None

        parsed_arg = await asyncio.get_running_loop().run_in_executor(
            None, _parse_expr
        )

        if isinstance(parsed_arg, bool):
            return argument, None

        return argument, parsed_arg
