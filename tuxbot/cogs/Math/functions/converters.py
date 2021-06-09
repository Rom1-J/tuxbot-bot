from typing import Any, Dict

from discord.ext import commands
from discord.ext.commands import Context

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

abc_dict: Dict[str, Any] = {}
functions_dict: Dict[str, Any] = {}
core_dict: Dict[str, Any] = {}

# pylint: disable=exec-used
exec("from sympy.abc import *", abc_dict)
exec("from sympy.functions import *", functions_dict)
exec("from sympy.core import *", core_dict)

global_dict = abc_dict | functions_dict | core_dict

del global_dict["__builtins__"]


class LatexConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        latex = argument.rstrip("`").lstrip("`")

        if not argument.startswith("$$"):
            latex = "$$" + latex

        if not argument.endswith("$$"):
            latex = latex + "$$"

        return latex


class ExprConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        argument = argument.rstrip("`").lstrip("`")

        if "_" in argument:
            return argument, None

        def _parse_expr():
            try:
                return parse_expr(
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

        parsed_arg = await ctx.bot.loop.run_in_executor(None, _parse_expr)

        if isinstance(parsed_arg, bool):
            return argument, None

        return argument, parsed_arg
