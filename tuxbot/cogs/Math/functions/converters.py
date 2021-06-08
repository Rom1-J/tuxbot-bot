from discord.ext import commands
from discord.ext.commands import Context

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)


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

        def _parse_expr():
            return parse_expr(
                argument,
                transformations=(
                    standard_transformations
                    + (implicit_multiplication_application,)
                ),
                evaluate=False,
            )

        parsed_arg = await ctx.bot.loop.run_in_executor(None, _parse_expr)

        return argument, parsed_arg
