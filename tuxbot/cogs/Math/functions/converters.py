from discord.ext import commands
from discord.ext.commands import Context


class LatexConverter(commands.Converter):
    async def convert(self, ctx: Context, argument: str):  # skipcq: PYL-W0613
        latex = argument.rstrip("`").lstrip("`")

        if not argument.startswith("$$"):
            latex = "$$" + latex

        if not argument.endswith("$$"):
            latex = latex + "$$"

        return latex
